---
disable-model-invocation: true
name: ars-ru-paper
description: ARS RU paper entrypoint — русская научная статья, аннотация, revision, ГОСТ
---

First invoke the Skill tool with `skill: "academic-research-skills:akademicheskaya-statya"`. Pass the user's request as its arguments; use the loaded skill and its supporting files before producing the result.

Trigger the `akademicheskaya-statya` skill.

Use this entrypoint for Russian academic writing tasks: план статьи, структура, черновик, аннотация, keywords, литературный обзор как раздел статьи, revision, response to reviewers, citation-check, ГОСТ/APA/IEEE/Vancouver conversion, disclosure statements.

Do not use this entrypoint for standalone research without a writing deliverable, independent peer review, or full pipeline orchestration. Route those to `/ars-ru-research`, `/ars-ru-reviewer`, or `/ars-ru-pipeline`.

For EN/RU/mixed requests, follow `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md`: use the Russian writing skill for Russian venue/context, ГОСТ, ВАК or РИНЦ requirements even when some sources or the final abstract are English; keep requested international citation styles when the venue requires them.

Skill entry: `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskaya-statya/SKILL.md`.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md`.
Resolve resources from `${CLAUDE_PLUGIN_ROOT}`, not the manuscript working directory. If a required skill/file cannot be loaded, report the failure and stop; do not replace it with this command summary.
