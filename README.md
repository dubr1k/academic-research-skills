# Academic Research Skills Bilingual Fork

[![Upstream](https://img.shields.io/badge/upstream-Imbad0202%2Facademic--research--skills-blue)](https://github.com/Imbad0202/academic-research-skills)
[![Snapshot](https://img.shields.io/badge/snapshot-v3.12.0%20%2F%20175f79b-lightgrey)](https://github.com/Imbad0202/academic-research-skills/commit/175f79bcca4467949fa94e410c25823bd574f687)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

This fork keeps the original English Academic Research Skills package and adds a Russian academic context layer.

Этот форк сохраняет исходный англоязычный пакет Academic Research Skills и добавляет русскоязычный академический слой.

## Choose Language

- English users: start with [README.en.md](README.en.md).
- Русскоязычные пользователи: начните с [README.ru.md](README.ru.md).
- Mixed RU/EN workflows: use [docs/bilingual-routing.md](docs/bilingual-routing.md).

## Skill Sets

English upstream skills:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Russian context skills:

- `akademicheskoe-issledovanie`
- `akademicheskaya-statya`
- `akademicheskii-retsenzent`
- `akademicheskii-konveer`

The plugin bundle now exposes both sets through [skills](skills/): the 4 upstream English skills and the 4 Russian adapters. Use `/ars-*` commands for English/international workflows and `/ars-ru-*` commands for Russian-context workflows.

## Routing Rule

Use the language and academic venue context together:

- English request + international venue -> upstream English skills.
- Russian request + Russian venue, ГОСТ, ВАК, РИНЦ/eLIBRARY or CyberLeninka -> Russian skills.
- Russian request + international venue -> Russian skill for planning/context, but preserve requested international format such as APA, IEEE, Vancouver or Chicago.
- English request + Russian venue/GOST/VAK/RINC -> Russian context skill, with output language decided by the user request.
- Mixed-language corpus -> keep source language metadata and do not translate titles or quotations unless asked.

Detailed rules and fixtures are in [docs/bilingual-routing.md](docs/bilingual-routing.md).

## Current Russian Adaptation

The Russian layer currently includes compact `SKILL.md` adapters under [russian-academic-skills](russian-academic-skills/). They adapt the upstream ideas for:

- ГОСТ Р 7.0.5-2008 bibliography expectations;
- ВАК/РИНЦ and Russian journal review context;
- eLIBRARY and CyberLeninka source handling;
- Russian academic style and AI-cliche checks;
- Opencode `task()` orchestration.

The parity map is tracked in [docs/skill-parity-matrix.md](docs/skill-parity-matrix.md).

Russian academic conventions are tracked in [docs/russian-academic-context.md](docs/russian-academic-context.md), with prompt examples in [examples/ru](examples/ru/) and [examples/bilingual](examples/bilingual/).

Each Russian adapter also ships local `references/` and `templates/` assets for ГОСТ bibliography, source verification, ВАК/РИНЦ review, traceability, and bilingual pipeline handoffs.

## Plugin Packaging

This fork ships as one bilingual bundle. Legacy Claude plugin metadata lives in [.claude-plugin](.claude-plugin/), and Codex-compatible metadata lives in [.codex-plugin](.codex-plugin/).

## Maintenance

The English upstream core should stay close to `Imbad0202/academic-research-skills`. Russian skills are maintained as an adapter layer and updated after upstream syncs.

The active implementation plan is [PLAN.md](PLAN.md).

## Upstream Integrity Notes

The fork keeps upstream integrity controls active. Stage 1 still records `experiment_intake_declaration` for experiment-backed or literature-only runs, and the opt-in Socratic reading-check probe is still controlled by `ARS_SOCRATIC_READING_PROBE=1`.

## License And Attribution

Original project: [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

License: Creative Commons Attribution-NonCommercial 4.0 International.

This fork is an adaptation distributed under compatible CC BY-NC 4.0 terms with attribution retained.
