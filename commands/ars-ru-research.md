---
description: ARS RU research entrypoint — русское исследование, обзор литературы, fact-check
---

Trigger the `akademicheskoe-issledovanie` skill.

Use this entrypoint for Russian academic research tasks: обзор литературы, systematic review, meta-analysis, fact-check, проверка источников, формулировка research question, ВАК/РИНЦ/eLIBRARY/CyberLeninka context, ГОСТ-oriented source handling.

Do not use this entrypoint when the user only needs manuscript writing, peer review, or the full research-to-publication workflow. Route those to `/ars-ru-paper`, `/ars-ru-reviewer`, or `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `docs/bilingual-routing.md`: choose the Russian skill when Russian venue/context, ГОСТ, ВАК, РИНЦ, eLIBRARY or CyberLeninka matters; preserve source-language metadata and do not translate titles or quotations unless requested.

Skill entry: `russian-academic-skills/akademicheskoe-issledovanie/SKILL.md`.
