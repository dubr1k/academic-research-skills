# Двуязычный форк Academic Research Skills

[![Upstream](https://img.shields.io/badge/upstream-Imbad0202%2Facademic--research--skills-blue)](https://github.com/Imbad0202/academic-research-skills)
[![Version](https://img.shields.io/badge/version-v3.23.0-blue)](https://github.com/Imbad0202/academic-research-skills/releases/tag/v3.23.0)
[![Snapshot](https://img.shields.io/badge/snapshot-v3.23.0%20%2F%206ab4b03-lightgrey)](https://github.com/Imbad0202/academic-research-skills/commit/6ab4b03bf70a118a1b3ee7f3263ed9f19031061b)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20696614-blue)](https://doi.org/10.5281/zenodo.20696614)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

Этот форк сохраняет актуальное англоязычное ядро Academic Research Skills и добавляет русскоязычный академический слой для ГОСТ, ВАК, РИНЦ/eLIBRARY, CyberLeninka и смешанных RU/EN сценариев.

## Выбор языка

[Русская документация](README.ru.md) | [English/upstream documentation](README.en.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md) | [Español](README.es-ES.md)

## Наборы навыков

Англоязычное upstream-ядро:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`
- `sr-screener` — протокольный отбор исследований для систематических обзоров

Русскоязычные adapter skills:

- `akademicheskoe-issledovanie`
- `akademicheskaya-statya`
- `akademicheskii-retsenzent`
- `akademicheskii-konveer`

Единый bilingual plugin bundle публикует все девять skills. Для international workflows используйте `/ars-*`, для российского академического контекста — `/ars-ru-*`.

## Правило маршрутизации

- English request + international venue → upstream English skill.
- Русский запрос + ГОСТ/ВАК/РИНЦ/eLIBRARY/CyberLeninka → русский adapter.
- Русский запрос + international venue → русский adapter для контекста, но формат целевого журнала имеет приоритет.
- English request + Russian venue → русский context adapter, язык ответа задает пользователь.
- Mixed corpus → сохраняйте `source_language`; не переводите названия и прямые цитаты без запроса.

Подробности: [bilingual routing](docs/bilingual-routing.md), [skill parity matrix](docs/skill-parity-matrix.md), [Russian academic context](docs/russian-academic-context.md).

## Что синхронизировано с upstream v3.23.0

- модельное разделение judgment/execution, opt-in tiering и усиленные cross-model checkpoints;
- риск-стратифицированная проверка утверждений, scope bindings и классификация novelty claims;
- независимый re-review judge и фиксированная пятикомпонентная reviewer panel;
- staleness advisory для citation cache с opt-in live re-validation;
- PDF read-integrity preflight, anchor-aware finalization и attestation фактического `read_scope`;
- canonical cross-model handoff, degradation registry и уточнённые границы Stage 5/6.
- revision-round claim-drift guards: claim-strength ladder, token conservation и hash-bound patch/apply-report custody;
- role-scoped reviewer scoring, typed evidence anchors, Coverage Receipts и canonical decision contract;
- трехфазный Stage 3' re-review: revision-blind criteria commitment → persuasion-blind evidence verdict → response-letter claim matching.
- bounded research-workflow profiles с `profile_binding`, field-general fail-closed fallback и явной фиксацией unresolved discipline fit;
- Stage Capability Matrix, Risk Register, Data Flows и Control Availability: проверяемые границы доказательств, сетевых вызовов и механизмов по каналам установки;
- consent-bound Claim-Standing Probe как advisory-only слой вне Phase E integrity result, с freshness и transmission ledger;
- process-isolated optional PDF text/OCR advisory и защищённый Codex subscription transport для citation-integrity без расширения scope на manuscript review.

Новые возможности v3.22–v3.23: протокольный `sr-screener` (dual review, QC, PRISMA), run ledger/handoff с сохранением пользовательских ограничений, language-pair contract, acronym check и исправления Windows/Pi/экспорта CSV. Русский слой поясняет RU/EN screening и восстановление выбора пользователя; Phase-1 registry пока не поддерживает `ru-en`, готовый русский locale pack не заявляется.

Русские adapters переносят эти механизмы содержательно: сохраняют российский venue/source context, не ослабляют integrity gates и различают optional hook hardening от обязательной проверки содержания.

Сохранены и более ранние upstream integrity contracts: Stage 1 фиксирует `experiment_intake_declaration` как для experiment-backed, так и для literature-only runs; opt-in Socratic reading-check включается только через `ARS_SOCRATIC_READING_PROBE=1`. Русский слой не меняет их семантику.

## Проверяемые upstream-контракты

- Reviewer panel: `(Journal-Fit Reviewer + 3 dynamic reviewers + Devil's Advocate)`; full mode (Journal-Fit Reviewer + R1/R2/R3 + Devil's Advocate).
- First-round review panel vs. contract-governed re-review dispatch boundary: повторная проверка использует отдельный contract-governed dispatch, а не автоматически восстанавливает состав первого раунда.
- Current live reviews remain `NOT_CALIBRATED`; the typed trajectory carrier is deferred. Confidence остаётся disclosure uncertainty/scope, а не весом или баллом.
- Citation integrity использует a deterministic citation-existence verification gate; revision integrity — a deterministic numeric/citation token-conservation checker.
- Зафиксированное измерение wording advisory: held-out miss rate 0.34–0.38 → 0.094 with false-fire 0/16 preserved. Это ограниченное историческое measurement, не универсальная гарантия эффективности.
- Optional write-scope guard: if no real Python is found it cleanly no-ops and the guard is simply inactive. Если поставляемый Python найден, но повреждён, the guard is inactive and the `PreToolUse` hook will log an error per call rather than no-op quietly.
- Нормативные карты: [docs/STAGE_CAPABILITY_MATRIX.md](docs/STAGE_CAPABILITY_MATRIX.md), [docs/RISK_REGISTER.md](docs/RISK_REGISTER.md), [docs/DATA_FLOWS.md](docs/DATA_FLOWS.md), [docs/CONTROL_AVAILABILITY.md](docs/CONTROL_AVAILABILITY.md).
- Venue disclosure selector различает ACL, BMJ, Chinese Nursing Journals Publishing House, EMNLP, Frontiers, ICLR, ICMJE, International Eye Science, JAMA, Nature, NEJM, NeurIPS, PLOS, Science и The Lancet; актуальная policy страницы venue имеет приоритет над встроенным профилем.

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
