---
disable-model-invocation: true
name: ars-ru-research
description: ARS RU research entrypoint — русское исследование, обзор литературы, fact-check
---

First invoke the Skill tool with `skill: "academic-research-skills:akademicheskoe-issledovanie"`. Pass the user's request as its arguments; use the loaded skill and its supporting files before producing the result.

Trigger the `akademicheskoe-issledovanie` skill.

Use this entrypoint for Russian academic research tasks: обзор литературы, systematic review, meta-analysis, fact-check, проверка источников, формулировка research question, ВАК/РИНЦ/eLIBRARY/CyberLeninka context, ГОСТ-oriented source handling.

Do not use this entrypoint when the user only needs manuscript writing, peer review, or the full research-to-publication workflow. Route those to `/ars-ru-paper`, `/ars-ru-reviewer`, or `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md`: choose the Russian skill when Russian venue/context, ГОСТ, ВАК, РИНЦ, eLIBRARY or CyberLeninka matters; preserve source-language metadata and do not translate titles or quotations unless requested.

Skill entry: `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskoe-issledovanie/SKILL.md`.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md`.
Resolve resources from `${CLAUDE_PLUGIN_ROOT}`, not the manuscript working directory. If a required skill/file cannot be loaded, report the failure and stop; do not replace it with this command summary.
