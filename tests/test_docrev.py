import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import docrev


def test_new_extract_status(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(docrev, "ROOT", tmp_path)
    docrev.new("demo")
    task = next((tmp_path / "tasks").iterdir())
    doc = pymupdf.open()
    doc.new_page().insert_text((72, 72), "Diffusion Policy for visuomotor control")
    doc.save(task / "sources" / "chi2023.pdf")
    (task / "notes" / "chi2023.md").write_text("---\nstatus: triaged\n---\n", encoding="utf-8")

    docrev.extract(task)
    docrev.extract(task)  # second run must not overwrite
    assert "Diffusion Policy" in (task / ".build/papers/chi2023/paper.md").read_text(encoding="utf-8")
    docrev.status(task)
    out = capsys.readouterr().out
    assert "skip chi2023.pdf" in out and "triaged" in out
