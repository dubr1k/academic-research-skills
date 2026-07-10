# Двуязычный форк Academic Research Skills

[![Upstream](https://img.shields.io/badge/upstream-Imbad0202%2Facademic--research--skills-blue)](https://github.com/Imbad0202/academic-research-skills)
[![Version](https://img.shields.io/badge/version-v3.15.0-blue)](https://github.com/Imbad0202/academic-research-skills/releases/tag/v3.15.0)
[![Snapshot](https://img.shields.io/badge/snapshot-v3.15.0%20%2F%20ad0a775-lightgrey)](https://github.com/Imbad0202/academic-research-skills/commit/ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20696614-blue)](https://doi.org/10.5281/zenodo.20696614)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

Этот форк сохраняет актуальное англоязычное ядро Academic Research Skills и добавляет русскоязычный академический слой для ГОСТ, ВАК, РИНЦ/eLIBRARY, CyberLeninka и смешанных RU/EN сценариев.

## Выбор языка

[Русская документация](README.ru.md) | [English/upstream documentation](README.en.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md)

## Наборы навыков

Англоязычное upstream-ядро:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Русскоязычные adapter skills:

- `akademicheskoe-issledovanie`
- `akademicheskaya-statya`
- `akademicheskii-retsenzent`
- `akademicheskii-konveer`

Единый bilingual plugin bundle публикует все восемь skills. Для international workflows используйте `/ars-*`, для российского академического контекста — `/ars-ru-*`.

## Правило маршрутизации

- English request + international venue → upstream English skill.
- Русский запрос + ГОСТ/ВАК/РИНЦ/eLIBRARY/CyberLeninka → русский adapter.
- Русский запрос + international venue → русский adapter для контекста, но формат целевого журнала имеет приоритет.
- English request + Russian venue → русский context adapter, язык ответа задает пользователь.
- Mixed corpus → сохраняйте `source_language`; не переводите названия и прямые цитаты без запроса.

Подробности: [bilingual routing](docs/bilingual-routing.md), [skill parity matrix](docs/skill-parity-matrix.md), [Russian academic context](docs/russian-academic-context.md).

## Что синхронизировано с upstream v3.15.0

- Socratic adjacent-framing probe для расширения соседних исследовательских рамок;
- deterministic write-scope guard и Windows/Python graceful degradation;
- OpenAlex API-key authentication, budget-aware handling `429` и arXiv ToU-aligned backoff;
- явные plugin skill paths, setup parity и новые release/command invariant gates;
- `THIRD_PARTY.md`, Korean README и актуальные release/attribution surfaces.

Русские adapters переносят эти механизмы содержательно: сохраняют российский venue/source context, не ослабляют integrity gates и различают optional hook hardening от обязательной проверки содержания.

Сохранены и более ранние upstream integrity contracts: Stage 1 фиксирует `experiment_intake_declaration` как для experiment-backed, так и для literature-only runs; opt-in Socratic reading-check включается только через `ARS_SOCRATIC_READING_PROBE=1`. Русский слой не меняет их семантику.

## Установка и требования

Полная upstream-инструкция: [docs/SETUP.md](docs/SETUP.md). Русская инструкция и примеры: [README.ru.md](README.ru.md).

Ядро prompt-driven и не требует Python. Реальный Python нужен для optional write-scope guard и некоторых opt-in команд; на Windows launcher использует Git Bash и безопасно отключает guard при отсутствии рабочего Python. Отсутствие optional guard не отменяет claim/citation/source verification.

## Упаковка и сопровождение

- Claude plugin metadata: [.claude-plugin](.claude-plugin/)
- Codex-compatible metadata: [.codex-plugin](.codex-plugin/)
- Upstream sync protocol: [docs/upstream-sync.md](docs/upstream-sync.md)
- Context gaps: [docs/context-adaptation-audit.md](docs/context-adaptation-audit.md)
- Third-party integrations: [THIRD_PARTY.md](THIRD_PARTY.md) (community-submitted; не являются endorsement upstream maintainer или автора адаптации)

Англоязычное ядро остается близким к `Imbad0202/academic-research-skills`; русские возможности поддерживаются отдельно и не удаляются при синхронизации.

## Лицензия и атрибуция

Исходный проект: [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills), Cheng-I Wu. Лицензия: Creative Commons Attribution-NonCommercial 4.0 International.

Русская адаптация: dubr1k. Форк распространяется на совместимых условиях CC BY-NC 4.0 с сохранением исходной атрибуции. Дополнительные заимствования и атрибуции перечислены в [THIRD_PARTY.md](THIRD_PARTY.md).
