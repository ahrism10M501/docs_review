"""Task folders for paper study: create, extract PDFs to Markdown, show progress."""

import argparse
from contextlib import redirect_stdout
from datetime import date
import io
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
GOAL = """# 학습 목표

- 왜 읽나:
- 다 읽고 나면 할 수 있어야 하는 것:
- 이미 아는 것:
- 낯선 것:
- 분야·렌즈: (예: 기본 / domain-lenses 4절 / physical-ai-lens)
- 깊이·시간: (예: 핵심 2편 정독, 나머지 훑기 / 주 3시간)
"""


def new(slug):
    task = ROOT / "tasks" / f"{date.today():%y%m%d}-{slug}"
    if task.exists():
        sys.exit(f"이미 있음: {task}")
    for name in ("sources", "notes", "deep"):
        (task / name).mkdir(parents=True)
    (task / "goal.md").write_text(GOAL, encoding="utf-8")
    print(task.relative_to(ROOT))


def extract(task):
    import pymupdf
    task = Path(task).resolve()
    for pdf in sorted((task / "sources").glob("*.pdf")):
        out = task / ".build" / "papers" / pdf.stem
        if out.exists():
            print(f"skip {pdf.name} (지우면 다시 추출)")
            continue
        (out / "media").mkdir(parents=True)
        # pymupdf4llm prints a layout-package hint on import; keep output clean.
        with redirect_stdout(io.StringIO()):
            import pymupdf4llm
            with pymupdf.open(pdf) as doc:
                chunks = pymupdf4llm.to_markdown(doc, write_images=True, image_path=(out / "media").as_posix(),
                                                 page_chunks=True, dpi=150)
        text = "\n\n".join(f"<!-- p.{i} -->\n\n{c['text']}" for i, c in enumerate(chunks, 1))
        (out / "paper.md").write_text(text.replace((out / "media").as_posix() + "/", "media/"), encoding="utf-8")
        print(f"ok   {pdf.name}: {len(chunks)}p -> {out.relative_to(task)}/paper.md")


def status(task):
    task = Path(task).resolve()
    print(f"{'paper':40} extracted  note  deep  status")
    for pdf in sorted((task / "sources").glob("*.pdf")):
        note = task / "notes" / f"{pdf.stem}.md"
        state = re.search(r"^status:\s*(\S+)", note.read_text(encoding="utf-8"), re.M) if note.exists() else None
        print(f"{pdf.stem[:40]:40} {'O' if (task / '.build/papers' / pdf.stem).exists() else '-':9}  "
              f"{'O' if note.exists() else '-':4}  {'O' if (task / 'deep' / pdf.stem).exists() else '-':4}  "
              f"{state[1] if state else '-'}")
    for name in ("synthesis.md", "glossary.md", "study.md"):
        print(f"{name:14} {'O' if (task / name).exists() else '-'}")


def main():
    parser = argparse.ArgumentParser(prog="docrev")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("new", help="tasks/<YYMMDD-slug> 만들기").add_argument("slug")
    for cmd in ("extract", "status"):
        sub.add_parser(cmd).add_argument("task")
    args = parser.parse_args()
    {"new": lambda: new(args.slug), "extract": lambda: extract(args.task), "status": lambda: status(args.task)}[args.cmd]()


if __name__ == "__main__":
    main()
