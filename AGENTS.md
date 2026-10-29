# docs_review 공통 지침

한 주제의 논문·문서를 `tasks/`에 모아 요약·비교·정독하고, 그 과정에서 사용자가 직접 학습하도록 돕는 하네스다. Claude Code·Codex·Gemini 공통이며 `CLAUDE.md`, `GEMINI.md`는 이 파일을 가리킨다.

## 무엇을 읽을까

| 하려는 일 | 시작점 |
| --- | --- |
| task 만들기·카드·비교·읽는 순서·학습 질문 | [paper-study](skills/paper-study/SKILL.md) |
| 논문 한 편 정독 보고서 | [paper-deep-reader](skills/paper-deep-reader/SKILL.md) (paper-study 5단계의 설정으로 호출) |
| 분야별로 논문을 볼 관점(렌즈) | paper-study의 "렌즈 고르기" (로봇·피지컬 AI는 [physical-ai-lens](skills/paper-study/references/physical-ai-lens.md)) |

명령: `uv run tools/docrev.py new <slug> | extract tasks/<task> | status tasks/<task>`. 테스트: `uv run --group dev pytest`.

## 지킬 것

- 수치·결과·인용·저자 정보를 만들지 않는다. 논문에 있는 것만 페이지와 함께 쓴다.
- `sources/`의 원본은 수정하지 않는다. 내려받기는 URL을 보여 주고 확인받는다.
- 외부 스킬 `skills/paper-deep-reader/`는 원문 그대로 둔다. 출처·커밋·해시는 `skills/dependencies.yaml`. 바꿀 것은 paper-study에서 덮어쓴다.
- 산출물은 한국어. 용어는 처음 나올 때 원어를 괄호로 병기한다.
- 실제 task 내용을 외부 서비스(Graphify 등)에 넣지 않는다.

## 발표로 이어갈 때

정독 보고서와 `synthesis.md`는 `~/workspace/ppt-gener` task의 `sources/`에 넣어 논문 리뷰 발표의 근거로 쓸 수 있다.
