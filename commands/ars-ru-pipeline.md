---
disable-model-invocation: true
name: ars-ru-pipeline
description: ARS RU pipeline entrypoint — русский research → paper → review → revision workflow
---

First invoke the Skill tool with `skill: "academic-research-skills:akademicheskii-konveer"`. Pass the user's request as its arguments; use the loaded skill and its supporting files before producing the result.

Trigger the `akademicheskii-konveer` skill.

Use this entrypoint when the user wants a full or partial Russian-context publication workflow: topic to research plan, literature review to manuscript, draft to integrity check, peer review, revision, re-review, final ГОСТ/disclosure package.

Do not use this entrypoint for a single isolated step such as only fact-checking, only an abstract, only citation conversion, or only peer review. Route those to `/ars-ru-research`, `/ars-ru-paper`, or `/ars-ru-reviewer`.

For EN/RU/mixed requests, follow `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md`: orchestrate Russian skills when Russian venue/context, ГОСТ, ВАК, РИНЦ/eLIBRARY or CyberLeninka matters; preserve international journal requirements when the Russian-language user is targeting an international venue.

Skill entry: `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskii-konveer/SKILL.md`.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md`.
Resolve resources from `${CLAUDE_PLUGIN_ROOT}`, not the manuscript working directory. If a required skill/file cannot be loaded, report the failure and stop; do not replace it with this command summary.
