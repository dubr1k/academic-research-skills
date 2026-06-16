---
description: ARS RU pipeline entrypoint — русский research → paper → review → revision workflow
---

Trigger the `akademicheskii-konveer` skill.

Use this entrypoint when the user wants a full or partial Russian-context publication workflow: topic to research plan, literature review to manuscript, draft to integrity check, peer review, revision, re-review, final ГОСТ/disclosure package.

Do not use this entrypoint for a single isolated step such as only fact-checking, only an abstract, only citation conversion, or only peer review. Route those to `/ars-ru-research`, `/ars-ru-paper`, or `/ars-ru-reviewer`.

For EN/RU/mixed requests, follow `docs/bilingual-routing.md`: orchestrate Russian skills when Russian venue/context, ГОСТ, ВАК, РИНЦ/eLIBRARY or CyberLeninka matters; preserve international journal requirements when the Russian-language user is targeting an international venue.

Skill entry: `russian-academic-skills/akademicheskii-konveer/SKILL.md`.
