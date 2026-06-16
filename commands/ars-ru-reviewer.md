---
description: ARS RU reviewer entrypoint — русская peer review, ВАК/РИНЦ, re-review
---

Trigger the `akademicheskii-retsenzent` skill.

Use this entrypoint for independent Russian-context review: pre-submission peer review, methodology review, ВАК/РИНЦ/journal fit, editorial decision simulation, re-review after revision, проверка закрытия замечаний.

Do not use this entrypoint to write or rewrite the manuscript. For revision writing route to `/ars-ru-paper`; for end-to-end workflow route to `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `docs/bilingual-routing.md`: use this reviewer when Russian academic venue, ГОСТ/ВАК/РИНЦ expectations, or Russian-language scholarly style affects the review; keep the output language aligned with the user's request.

Skill entry: `russian-academic-skills/akademicheskii-retsenzent/SKILL.md`.
