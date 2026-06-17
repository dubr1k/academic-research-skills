# Двуязычный форк Academic Research Skills

[![Upstream](https://img.shields.io/badge/upstream-Imbad0202%2Facademic--research--skills-blue)](https://github.com/Imbad0202/academic-research-skills)
[![Version](https://img.shields.io/badge/version-v3.12.1-blue)](https://github.com/Imbad0202/academic-research-skills/releases/tag/v3.12.1)
[![Snapshot](https://img.shields.io/badge/snapshot-v3.12.1%20%2F%2088fc003-lightgrey)](https://github.com/Imbad0202/academic-research-skills/commit/88fc003e6abf5fe9fe86dc8200f8d4aa8d511956)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20696614.svg)](https://doi.org/10.5281/zenodo.20696614)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

Этот форк сохраняет исходное англоязычное ядро Academic Research Skills и добавляет русскоязычный академический слой для ГОСТ, ВАК, РИНЦ/eLIBRARY, CyberLeninka и смешанных RU/EN рабочих сценариев.

## Выбор языка

- Русскоязычные пользователи: начните с [README.ru.md](README.ru.md).
- English users: use [README.en.md](README.en.md).
- Смешанные RU/EN задачи: используйте [docs/bilingual-routing.md](docs/bilingual-routing.md).

## Наборы навыков

Англоязычное upstream-ядро:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Русскоязычные адаптеры контекста:

- `akademicheskoe-issledovanie`
- `akademicheskaya-statya`
- `akademicheskii-retsenzent`
- `akademicheskii-konveer`

Пакет плагина публикует оба набора через [skills](skills/): четыре upstream English skills и четыре русских adapter skills. Для English/international workflows используйте `/ars-*`, для русского академического контекста используйте `/ars-ru-*`.

## Правило маршрутизации

Выбор навыка зависит не только от языка запроса, но и от академического контекста:

- English request + international venue -> upstream English skills.
- Русский запрос + российский журнал, ГОСТ, ВАК, РИНЦ/eLIBRARY или CyberLeninka -> русские skills.
- Русский запрос + international venue -> русский skill для планирования и контекста, но итоговый формат сохраняет APA, IEEE, Vancouver, Chicago или другое требование журнала.
- English request + Russian venue/GOST/VAK/RINC -> русский context skill, а язык ответа определяется запросом пользователя.
- Mixed-language corpus -> сохранять `source_language`, не переводить названия источников и прямые цитаты без явной просьбы.

Подробные правила и fixtures находятся в [docs/bilingual-routing.md](docs/bilingual-routing.md).

## Текущее состояние русской адаптации

Русский слой находится в [russian-academic-skills](russian-academic-skills/) и адаптирует upstream workflow под:

- ГОСТ Р 7.0.5-2008 и библиографические проверки;
- ВАК/РИНЦ и российский журнальный контекст;
- eLIBRARY и CyberLeninka source handling;
- русскую академическую стилистику и AI-cliche checks;
- Opencode `task()` orchestration;
- traceability для reviewer response и bilingual handoffs.

Матрица соответствия upstream skills и русских adapters ведется в [docs/skill-parity-matrix.md](docs/skill-parity-matrix.md).

Российские академические правила описаны в [docs/russian-academic-context.md](docs/russian-academic-context.md), примеры запросов лежат в [examples/ru](examples/ru/) и [examples/bilingual](examples/bilingual/).

Каждый русский adapter уже содержит локальные `agents/`, `references/` и `templates/` для ГОСТ bibliography, source verification, ВАК/РИНЦ review, traceability и bilingual pipeline handoffs.

## Упаковка плагина

Форк распространяется как единый bilingual bundle. Legacy metadata для Claude Code находится в [.claude-plugin](.claude-plugin/), Codex-compatible metadata находится в [.codex-plugin](.codex-plugin/).

## Поддержка и развитие

Англоязычное upstream-ядро должно оставаться близким к `Imbad0202/academic-research-skills`. Русские skills поддерживаются как adapter layer и обновляются после upstream sync.

Покрытие разных академических контекстов и оставшиеся gaps отслеживаются в [docs/context-adaptation-audit.md](docs/context-adaptation-audit.md).

Активный план работ находится в [PLAN.md](PLAN.md).

## Целостность upstream

Форк сохраняет upstream integrity controls. Stage 1 по-прежнему записывает `experiment_intake_declaration` для experiment-backed и literature-only runs, а opt-in Socratic reading-check probe управляется через `ARS_SOCRATIC_READING_PROBE=1`.

## Лицензия и атрибуция

Исходный проект: [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills), автор Cheng-I Wu.

Лицензия: Creative Commons Attribution-NonCommercial 4.0 International.

Этот форк является адаптацией и распространяется на совместимых условиях CC BY-NC 4.0 с сохранением атрибуции.
