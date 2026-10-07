---
disable-model-invocation: true
name: ars-ru-reviewer
description: ARS RU reviewer entrypoint — русская peer review, ВАК/РИНЦ, re-review
---

First invoke the Skill tool with `skill: "academic-research-skills:akademicheskii-retsenzent"`. Pass the user's request as its arguments; use the loaded skill and its supporting files before producing the result.

Trigger the `akademicheskii-retsenzent` skill.

Use this entrypoint for independent Russian-context review: pre-submission peer review, methodology review, ВАК/РИНЦ/journal fit, editorial decision simulation, re-review after revision, проверка закрытия замечаний.

Do not use this entrypoint to write or rewrite the manuscript. For revision writing route to `/ars-ru-paper`; for end-to-end workflow route to `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md`: use this reviewer when Russian academic venue, ГОСТ/ВАК/РИНЦ expectations, or Russian-language scholarly style affects the review; keep the output language aligned with the user's request.

Skill entry: `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskii-retsenzent/SKILL.md`.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md`.
Resolve resources from `${CLAUDE_PLUGIN_ROOT}`, not the manuscript working directory. If a required skill/file cannot be loaded, report the failure and stop; do not replace it with this command summary.
