---
description: ARS RU paper entrypoint — русская научная статья, аннотация, revision, ГОСТ
---

Trigger the `akademicheskaya-statya` skill.

Use this entrypoint for Russian academic writing tasks: план статьи, структура, черновик, аннотация, keywords, литературный обзор как раздел статьи, revision, response to reviewers, citation-check, ГОСТ/APA/IEEE/Vancouver conversion, disclosure statements.

Do not use this entrypoint for standalone research without a writing deliverable, independent peer review, or full pipeline orchestration. Route those to `/ars-ru-research`, `/ars-ru-reviewer`, or `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `docs/bilingual-routing.md`: use the Russian writing skill for Russian venue/context, ГОСТ, ВАК or РИНЦ requirements even when some sources or the final abstract are English; keep requested international citation styles when the venue requires them.

Skill entry: `russian-academic-skills/akademicheskaya-statya/SKILL.md`.
