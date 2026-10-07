---
disable-model-invocation: true
name: ars-auto
description: ARS auto router — choose EN/RU academic skill from task context
---

Route the request to an existing ARS skill; do not do heavy academic work inside this command.

Use this entrypoint when the user provides an academic task without choosing an English `/ars-*` or Russian `/ars-ru-*` command.

Do not use this entrypoint when the user explicitly invoked `/ars-*` or `/ars-ru-*`, named a specific skill, or asked to bypass routing. In those cases, honor the selected command/skill and apply `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md` only for language, venue, citation, and source-language constraints inside that skill.

Apply `${CLAUDE_PLUGIN_ROOT}/docs/bilingual-routing.md` deterministically:

1. Classify the task as `research`, `paper`, `review`, or `pipeline`.
2. Detect request language: `en`, `ru`, or `mixed`.
3. Detect requested output language; default to the latest user request language unless manuscript/output language is explicit.
4. Detect venue/context: `international`, `Russian journal`, `ВАК`, `РИНЦ/eLIBRARY`, `CyberLeninka`, `dissertation council`, or `unspecified`.
5. Detect citation style: `APA`, `IEEE`, `Vancouver`, `Chicago`, `MLA`, `ГОСТ`, or `unspecified`.
6. Set `source_language` policy: `en_corpus`, `ru_corpus`, `mixed_corpus`, or `unspecified`; preserve original titles and quotations unless the user or target style requires translation/transliteration.
7. Select exactly one existing skill:

| Task | International / English context | Russian context |
|---|---|---|
| `research` | `deep-research` | `akademicheskoe-issledovanie` |
| `paper` | `academic-paper` | `akademicheskaya-statya` |
| `review` | `academic-paper-reviewer` | `akademicheskii-retsenzent` |
| `pipeline` | `academic-pipeline` | `akademicheskii-konveer` |

Before loading the selected skill, surface this routing header:

```text
Routing:
- selected_skill: <skill>
- request_language: <en|ru|mixed>
- output_language: <en|ru|bilingual|unspecified>
- venue: <detected venue/context>
- citation_style: <detected style>
- source_language: <policy>
- warnings: <none or concise warning list>
```

Warn when routing detects citation/venue conflicts:

- `ГОСТ` with an English manuscript or international venue: use the Russian-context skill, but warn that the target venue may require APA/IEEE/Vancouver/Chicago instead.
- `APA`, `IEEE`, `Vancouver`, or `Chicago` with a Russian venue requiring `ГОСТ`: use the Russian-context skill and warn that venue rules override generic style preference unless the user requested conversion/comparison.
- Russian prompt plus international style is not a conflict by itself; keep Russian interaction/output constraints while preserving the requested international citation style.
- Mixed source corpora are not a conflict by themselves; preserve source-language metadata and do not invent missing DOI, issue, pages, publisher, or translated titles.

Skill entries:

- `${CLAUDE_PLUGIN_ROOT}/deep-research/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/academic-paper-reviewer/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/academic-pipeline/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskoe-issledovanie/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskaya-statya/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskii-retsenzent/SKILL.md`
- `${CLAUDE_PLUGIN_ROOT}/russian-academic-skills/akademicheskii-konveer/SKILL.md`

After selecting exactly one skill, use its plugin namespace and basename, not its directory path. First invoke the Skill tool with `skill: "academic-research-skills:<selected_skill>"`. Pass the original request and routing constraints as arguments.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md`.
Resolve resources from `${CLAUDE_PLUGIN_ROOT}`, not the manuscript working directory. If a required skill/file cannot be loaded, report the failure and stop; do not replace it with this command summary.
