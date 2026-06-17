# План развития двуязычного форка Academic Research Skills

## Статус выполнения

### Выполнено в первом срезе

- Корневой `README.md` превращен в короткую двуязычную landing page.
- Текущий русский README сохранен как `README.ru.md`.
- Upstream README из snapshot `175f79bcca4467949fa94e410c25823bd574f687` добавлен как `README.en.md`.
- Добавлен `docs/bilingual-routing.md` с правилами EN/RU/mixed маршрутизации и 12 routing fixtures.
- Добавлен `docs/skill-parity-matrix.md` с матрицей соответствия upstream skills и русских adapters.
- Добавлен `tests/fixtures/bilingual_routing_cases.json`.
- Добавлен `tests/test_bilingual_docs.py`.
- Полный тестовый прогон прошел: `2707 passed, 1 xfailed, 127 subtests passed`.

### Выполнено во втором срезе (P1)

- Унифицирован frontmatter всех 4 русских `SKILL.md`.
- Добавлены обязательные metadata-поля: `name`, `description`, `version`, `last_updated`, `status`, `data_access_level`, `task_type`, `depends_on`, `upstream_snapshot`, `upstream_version`, `upstream_date`.
- Добавлены русские slash-command entrypoints: `/ars-ru-research`, `/ars-ru-paper`, `/ars-ru-reviewer`, `/ars-ru-pipeline`.
- Добавлен `docs/upstream-sync.md` с remote layout, sync workflow, snapshot update rules, plugin packaging decision и тестовым протоколом.
- Добавлен `tests/test_russian_entrypoints.py`.
- `.claude-plugin/*` проверены; русский слой задокументирован как manual adapter layer до отдельного plugin packaging среза.
- Полный тестовый прогон прошел: `2710 passed, 1 xfailed, 127 subtests passed`.

### Следующий срез

- Следующий upstream sync выполнять после нового upstream release поверх snapshot `88fc003e6abf5fe9fe86dc8200f8d4aa8d511956`.

## Что делаем дальше

Срез **P1 — формализовать русские entrypoints и metadata** выполнен. Этот раздел оставлен как архив критериев и решений P1.

### Выполнено в P2a — русский academic context и fixtures

- Добавлен `docs/russian-academic-context.md` с правилами ГОСТ, ВАК/РИНЦ, eLIBRARY, CyberLeninka, source verification, Russian AI-cliche checks и response traceability.
- Добавлены примеры `examples/ru/` и `examples/bilingual/` для research, paper, reviewer, pipeline и mixed Scopus/CyberLeninka workflows.
- Добавлен `tests/fixtures/russian_quality_cases.json` с lightweight quality fixtures.
- Добавлен `tests/test_russian_academic_context.py`.

### Выполнено в P2b — bilingual plugin packaging

- Принято решение: один bilingual plugin bundle вместо отдельного Russian plugin.
- В `skills/` добавлены 4 русских adapter entrypoints рядом с 4 upstream English skills.
- `.claude-plugin/plugin.json` и `.claude-plugin/marketplace.json` обновлены под bilingual bundle.
- Добавлен `.codex-plugin/plugin.json` для Codex-compatible metadata.
- Добавлен `tests/test_bilingual_plugin_packaging.py`.

### Выполнено в P2c — русские references/templates

- В каждый русский skill добавлен первый локальный `references/` asset.
- В каждый русский skill добавлен первый локальный `templates/` asset.
- `SKILL.md` каждого русского adapter теперь ссылается на свои локальные материалы.
- Добавлен `tests/test_russian_reference_templates.py`.

### Выполнено в P2d — русские agent prompts

- В каждый русский skill добавлен первый локальный `agents/` prompt.
- Research agent покрывает eLIBRARY/РИНЦ/CyberLeninka source verification.
- Writing agent покрывает ГОСТ citations и ВАК article package readiness.
- Reviewer agent покрывает ВАК/РИНЦ peer-review criteria.
- Pipeline agent покрывает bilingual state, handoffs и mandatory integrity gates.
- Добавлен `tests/test_russian_agents.py`.

### Выполнено в P2e — deep evals качества русского академического слоя

- Добавлен `evals/gold/russian_academic_quality/` как advisory-calibration gold set.
- Gold set покрывает ГОСТ bibliography, ВАК/РИНЦ status separation, eLIBRARY/CyberLeninka/DOI verification, русские academic cliches, revision traceability и mixed-language routing.
- Добавлены `manifest.yaml`, `gold_set.json` и README для нового eval-набора.
- Добавлен `tests/test_russian_academic_evals.py`.

### Выполнено в P2f — runtime measurer для русского academic quality eval

- Добавлен `scripts/check_russian_academic_quality.py`.
- `scripts/run_evals.py` теперь измеряет `russian_academic_quality` как native advisory-calibration task.
- Метрики: `advisory_recall`, `forbidden_action_rate` и label-level `guard_coverage`.
- Manifest `russian_academic_quality` указывает на `scripts.check_russian_academic_quality`.
- Добавлен `scripts/test_check_russian_academic_quality.py`.
- `scripts.run_evals --task russian_academic_quality` возвращает `status: measured`.

### Выполнено в P3a — audit контекстной адаптации репозитория

- Добавлен `docs/context-adaptation-audit.md`.
- Аудит связывает контекстные оси: EN/RU/mixed, venue, output language, citation style, `source_language`, verification и traceability.
- Зафиксированы поверхности, где уже есть адаптация: README, routing docs, Russian context docs, commands, plugin metadata, examples, evals и русские adapters.
- Зафиксирован backlog адаптации: Russian source verification, ГОСТ bibliography, ВАК/РИНЦ review, bilingual pipeline handoff, auto/router entrypoint и global shared agents.
- Добавлен `tests/test_context_adaptation_audit.py`.

### Выполнено в P3b — Russian source verification depth

- Углублен `russian_source_verifier_agent.md`: добавлена verification ladder и статусы `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, `rejected`.
- Расширен `references/russian-source-verification.md` правилами current status evidence, access-channel vs index/status distinction и handoff requirements.
- Расширен `templates/literature-matrix-gost.md` колонкой current status evidence и правилами сохранения `metadata_missing` / `not_verified`.
- Добавлены примеры `examples/ru/research-source-verification-depth.md` и `examples/bilingual/mixed-source-verification-handoff.md`.
- `russian_academic_quality` gold set расширен с 12 до 15 кейсов; source verification теперь покрывает eLIBRARY/РИНЦ/ВАК, неполные русские записи и mixed `source_language`.
- `docs/context-adaptation-audit.md` обновлен: P3b отмечен как covered in the first depth pass, следующий рекомендованный срез — P3c.

### Выполнено в P3c — ГОСТ bibliography и journal override depth

- `gost-bibliography-guide.md` расширен source-type patterns: journal article, monograph, dissertation abstract, conference paper и web source.
- Добавлены journal override rules: APA, IEEE, Vancouver, Chicago, локальный ГОСТ-вариант или style sheet журнала имеют приоритет над default ГОСТ.
- `gost_citation_agent.md` теперь фиксирует source type и Citation Style Decision: default style, override, final style и evidence.
- `vak-article-package.md` получил Citation Style Decision и journal override checks.
- Добавлены примеры `examples/ru/paper-gost-source-types.md` и `examples/bilingual/russian-journal-apa-override.md`.
- `russian_academic_quality` gold set расширен с 15 до 18 кейсов; `gost_bibliography` теперь покрывает разные типы источников, missing access date и российский APA override.

### Выполнено в P3d — ВАК/РИНЦ review и re-review traceability depth

- `vak-rinc-review-criteria.md` разделяет `journal-index status` и `manuscript quality`.
- Добавлены отдельные критерии для ВАК article, dissertation council и international journal review.
- `review-report-traceability.md` и `vak_rinc_reviewer_agent.md` закрепляют статусы `addressed`, `partially_addressed`, `not_addressed`, `needs_evidence`.
- Page/section-level manuscript evidence стало обязательным перед закрытием замечания как `addressed`.
- Добавлен пример `examples/ru/reviewer-rereview-traceability.md`.

### Выполнено в P3e — bilingual pipeline handoff и global shared agents

- `bilingual-handoff-contracts.md` расширен `source_verification_state`, `gate_carryover`, `checkpoint_carryover`, `output_language`, `source_language` и `final_package_mode`.
- `russian_pipeline_state_agent.md` и `pipeline-dashboard.md` теперь показывают source verification state, final package mode и shared/global agent audit.
- Добавлен `global_agent_norm_risk` для случаев, когда shared/global agent возвращает English-centric assumptions.
- Добавлен пример `examples/bilingual/pipeline-bilingual-handoff.md`.

### Выполнено в P3f — auto/router entrypoint

- Добавлена команда `commands/ars-auto.md`.
- `/ars-auto` применяет `docs/bilingual-routing.md` и выводит routing header: `selected_skill`, `request_language`, `output_language`, `venue`, `citation_style`, `source_language`, `warnings`.
- Router не создает новый тяжелый skill; он выбирает один из существующих EN/RU skills.
- `russian_academic_quality` gold set расширен с 18 до 22 кейсов: добавлены reviewer status separation, re-review taxonomy и bilingual pipeline final package mode.

### Выполнено в Post-P3a — LLM-output judged evals

- Добавлен `evals/gold/russian_academic_quality_judged/` как recorded-output judged layer поверх structural `russian_academic_quality`.
- Новый gold set содержит 6 `model_output` fixtures: по одному для ГОСТ bibliography, ВАК/РИНЦ status, source verification, Russian style, revision traceability и mixed-language routing.
- Добавлен `scripts/check_russian_academic_quality_judged.py` с метриками `judged_pass_rate` и `critical_failure_rate`.
- `scripts/run_evals.py` теперь измеряет `russian_academic_quality_judged` как native `llm-output-judged` task.
- `.github/workflows/eval-harness.yml` запускается при изменении русских quality checker scripts.

### Выполнено в Post-P3b — venue-specific examples

- Добавлены русские venue examples: `venue-vak-submission-package.md`, `venue-rinc-elibrary-status-check.md`, `venue-dissertation-council-review.md`.
- Добавлены bilingual venue examples: `venue-scopus-wos-russian-sources.md`, `venue-journal-override-final-package.md`.
- Примеры покрывают ВАК submission package, РИНЦ/eLIBRARY current status evidence, dissertation council review, Scopus/WoS article with Russian sources, APA journal override и `final_package_mode: bilingual`.
- `docs/context-adaptation-audit.md` обновлен: Post-P3b отмечен как covered in the first venue-specific pass.

### Выполнено в Post-P3c — upstream sync v3.12.1

- Выполнен `git fetch upstream` и merge `upstream/main`.
- Англоязычное ядро синхронизировано с upstream snapshot `88fc003e6abf5fe9fe86dc8200f8d4aa8d511956` (`v3.12.1`, 2026-06-17).
- `README.en.md` обновлен из upstream README.
- Bilingual `README.md`, `.claude-plugin/*`, `.codex-plugin/plugin.json` и plugin tests сохранены как bilingual fork overlay с версией `3.12.1`.
- Все русские adapters обновили `upstream_snapshot`, `upstream_version` и `upstream_date`.

### Выполнено в Post-P3d — candidate-output capture

- Добавлен `scripts/capture_russian_academic_quality_outputs.py`.
- `russian_academic_quality_judged` получил `candidate_outputs/baseline/*.md` и `manifest.json` с SHA-256 hash для каждого recorded `model_output`.
- Manifest `russian_academic_quality_judged` теперь указывает `target.candidate_output_dir: candidate_outputs/baseline`.
- Добавлен `--check` режим, который ловит drift между `gold_set.json` и captured candidate outputs.

### Выполнено в Post-P3e — cached judge verdict fixtures и dimension metrics

- Добавлен `judge_verdicts/baseline/` для `russian_academic_quality_judged`: по одному cached verdict JSON на каждый captured candidate output.
- Verdict fixtures фиксируют `verdict`, `dimension_results`, `hard_failures`, `candidate_path`, `candidate_sha256`, rationale и evidence quotes.
- `scripts/check_russian_academic_quality_judged.py` теперь валидирует cached verdicts и считает `dimension_pass_rate` и `needs_human_review_rate`.
- `scripts/run_evals.py` прокидывает `target.judge_verdict_dir` и выводит dimension metrics в per-class отчет.

### Выполнено в Post-P3f — negative и needs_human_review verdict calibration

- Добавлен non-gating `judge_verdicts/calibration/` для `russian_academic_quality_judged` с теми же six case IDs, что и baseline.
- Calibration set включает explicit `fail` hard failure `fabricated_source_verification` и explicit `needs_human_review` style-quality case.
- Manifest теперь указывает `target.judge_calibration_verdict_dir: judge_verdicts/calibration`.
- Тесты проверяют, что calibration verdicts снижают `judged_pass_rate`/`dimension_pass_rate` и не засчитывают `needs_human_review` как pass.

### Цель среза

Сделать так, чтобы русская часть была не только описана в документации, но и имела стабильные точки входа, проверяемые метаданные и понятный процесс обновления от upstream.

### Задачи по порядку

1. Унифицировать frontmatter во всех русских skills:
   - `russian-academic-skills/akademicheskoe-issledovanie/SKILL.md`;
   - `russian-academic-skills/akademicheskaya-statya/SKILL.md`;
   - `russian-academic-skills/akademicheskii-retsenzent/SKILL.md`;
   - `russian-academic-skills/akademicheskii-konveer/SKILL.md`.
2. Добавить обязательные поля:
   - `name`;
   - `description`;
   - `version`;
   - `last_updated`;
   - `depends_on`, если skill зависит от других skills;
   - `status`;
   - `data_access_level`;
   - `task_type`;
   - `upstream_snapshot`.
3. Добавить русские slash-command entrypoints в `commands/`:
   - `ars-ru-research.md`;
   - `ars-ru-paper.md`;
   - `ars-ru-reviewer.md`;
   - `ars-ru-pipeline.md`.
4. В каждом `/ars-ru-*` entrypoint явно указать:
   - какой русский skill использовать;
   - когда не использовать этот entrypoint;
   - как обрабатывать EN/RU/mixed запросы;
   - ссылку на `docs/bilingual-routing.md`.
5. Добавить `docs/upstream-sync.md`:
   - remote layout: `origin` и `upstream`;
   - порядок fetch/diff/merge;
   - как обновлять snapshot hash в русских skills;
   - какие тесты запускать после sync.
6. Проверить `.claude-plugin/plugin.json` и `.claude-plugin/marketplace.json`:
   - решить, оставляем ли один bilingual plugin;
   - или документируем Russian layer как manual install до отдельного plugin-среза.
7. Расширить тесты:
   - frontmatter русских skills содержит обязательные поля;
   - `/ars-ru-*` команды существуют;
   - команды ссылаются на правильные русские skills;
   - `docs/upstream-sync.md` упоминает `origin`, `upstream`, snapshot update и тесты.

### Критерии готовности

- Все 4 русских `SKILL.md` имеют одинаковую metadata-схему.
- Все 4 `/ars-ru-*` команды добавлены и документируют правильный skill routing.
- `docs/upstream-sync.md` описывает воспроизводимый процесс синхронизации.
- Новый тестовый файл покрывает frontmatter, команды и sync doc.
- Полный `pytest` проходит.
- После успешного теста `PLAN.md` обновлен с отметкой о выполнении P1-среза.

### Коммит

Ожидаемый commit scope:

```text
feat(russian): add ru command entrypoints and metadata checks
```

Если изменения будут только документационными и тестовыми, использовать:

```text
docs(russian): formalize ru entrypoints and sync workflow
```

## Цель

Сделать форк, который одновременно и предсказуемо поддерживает два рабочих контекста:

- английский академический контекст исходного проекта;
- русский академический контекст: ГОСТ, ВАК, РИНЦ/eLIBRARY, CyberLeninka, русские жанры и типичные языковые риски.

Форк не должен превращаться в разовый перевод. Нужна поддерживаемая архитектура: upstream можно обновлять, русские адаптеры можно развивать отдельно, а пользователь должен получать правильный навык по языку и задаче.

## Что уже адаптировано

Текущее состояние после клонирования `https://github.com/dubr1k/academic-research-skills`:

- исходные англоязычные skills сохранены: `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`;
- добавлен отдельный каталог `russian-academic-skills/`;
- добавлены 4 русскоязычных skill-файла:
  - `akademicheskoe-issledovanie` - исследование, обзор литературы, fact-check, systematic review;
  - `akademicheskaya-statya` - планирование, написание, ревизия, аннотация, оформление статьи;
  - `akademicheskii-retsenzent` - независимая рецензия, methodology review, re-review;
  - `akademicheskii-konveer` - полный workflow от темы до финального пакета;
- `README.md` переписан под русскоязычную адаптацию, установку для Claude Code и Opencode, правила выбора навыков и примеры запросов;
- русские skills учитывают ГОСТ Р 7.0.5-2008, ВАК/РИНЦ, eLIBRARY, CyberLeninka, русские academic cliches и Opencode `task()` orchestration;
- в каждом русском skill указан upstream snapshot `175f79bcca4467949fa94e410c25823bd574f687` (`v3.12.0`, 2026-06-08).

Ограничения текущей адаптации:

- русская часть пока компактный верхнеуровневый слой, а не полная локализация всех `agents/`, `references/`, `templates/`, `commands/`, `evals/`;
- нет единого bilingual routing layer, который формально решает: English skill, Russian skill или mixed-language workflow;
- нет тестов на выбор языка, выбор skill, ГОСТ-оформление, русские клише, mixed RU/EN сценарии;
- plugin metadata, slash commands и большая часть проверочных скриптов остаются ориентированы на исходный английский пакет;
- README стал русским входом, но не оформлен как двуязычная главная страница.

## Архитектурное решение

### 1. Сохранить upstream как английское ядро

Англоязычные каталоги остаются максимально близкими к upstream:

- `deep-research/`
- `academic-paper/`
- `academic-paper-reviewer/`
- `academic-pipeline/`
- `shared/`
- `agents/`
- `commands/`
- `scripts/`
- `evals/`

Правило: не переводить upstream in-place без необходимости. Это снижает стоимость merge из исходного проекта.

### 2. Русский контекст держать как adapter layer

Русский слой остается отдельным:

- `russian-academic-skills/akademicheskoe-issledovanie/`
- `russian-academic-skills/akademicheskaya-statya/`
- `russian-academic-skills/akademicheskii-retsenzent/`
- `russian-academic-skills/akademicheskii-konveer/`

Русские skills должны ссылаться на upstream-идеи, но описывать самостоятельные правила для русского контекста: ГОСТ, ВАК/РИНЦ, русская научная стилистика, локальные источники и ограничения.

### 3. Добавить bilingual routing layer

Нужен отдельный слой выбора:

- язык запроса: EN, RU, mixed;
- язык требуемого результата;
- академическая задача: research, writing, review, pipeline;
- локальный контекст: international journal или Russian/VAK/RINC context;
- стиль цитирования: APA/IEEE/Vancouver/Chicago/MLA/ГОСТ;
- необходимость перевода, bilingual abstract или cross-language literature review.

Возможные реализации:

- `BILINGUAL.md` или `docs/bilingual-routing.md` как правило для агентов;
- отдельный skill `academic-router` / `akademicheskii-router`;
- раздел в `AGENTS.md`/README для Claude Code и Opencode;
- тестовые fixtures для маршрутизации.

Рекомендуемое решение: начать с документа `docs/bilingual-routing.md`, затем добавить compact router skill только если routing начнет повторяться в нескольких местах.

## Этапы работ

### Этап 0. Репозиторная база

Задачи:

- добавить upstream remote: `https://github.com/Imbad0202/academic-research-skills`;
- зафиксировать policy: upstream changes мержатся в английское ядро, русские адаптеры обновляются вручную;
- добавить `README.en.md` с сохраненным английским описанием или ссылкой на upstream;
- превратить `README.md` в короткую двуязычную landing page;
- перенести текущий русский README в `README.ru.md`.

Результат:

- пользователь сразу понимает, что это bilingual fork;
- English users не теряют вход в исходный workflow;
- Russian users видят русскую установку и правила выбора skills.

### Этап 1. Матрица соответствия skills

Задачи:

- создать `docs/skill-parity-matrix.md`;
- сопоставить пары:
  - `deep-research` <-> `akademicheskoe-issledovanie`;
  - `academic-paper` <-> `akademicheskaya-statya`;
  - `academic-paper-reviewer` <-> `akademicheskii-retsenzent`;
  - `academic-pipeline` <-> `akademicheskii-konveer`;
- отметить, какие upstream capabilities уже перенесены, какие намеренно не перенесены, какие требуют русской адаптации;
- отдельно отметить features, которые не надо копировать без проверки: complex eval framework, agent contracts, disclosure policies, plugin hooks.

Результат:

- видно, где русская версия является адаптером, а где функционально отстает от upstream;
- проще обновлять русские skills после новых upstream releases.

### Этап 2. Правила bilingual routing

Задачи:

- описать routing algorithm:
  - RU request + Russian academic venue -> Russian skills;
  - EN request + international venue -> upstream English skills;
  - RU request + international journal -> Russian planning, international citation/output requirements;
  - EN request + Russian venue/GOST/VAK/RINC -> Russian context skill, output language per user;
  - mixed corpus -> research skill must keep source language metadata;
- определить default language policy:
  - отвечать на языке пользователя;
  - не переводить названия источников без необходимости;
  - сохранять оригинальные цитаты источников;
  - bilingual abstracts делать только по запросу или если это нужно журналу;
- добавить conflict rules:
  - ГОСТ vs APA/IEEE;
  - Russian journal requirements vs international journal requirements;
  - English manuscript with Russian sources;
  - Russian manuscript with English bibliography.

Результат:

- агент не выбирает русский skill только из-за кириллицы в одном источнике;
- mixed-language academic workflows становятся предсказуемыми.

### Этап 3. Доработка русских skills

Задачи:

- унифицировать frontmatter: `name`, `description`/`desc`, `version`, `last_updated`, `depends_on`, `status`;
- добавить явные language/output rules во все 4 русских skills;
- расширить `akademicheskoe-issledovanie`:
  - поиск по международным и российским источникам;
  - оценка статуса eLIBRARY/РИНЦ;
  - пометка peer-reviewed / non-peer-reviewed / inaccessible;
  - anti-hallucination protocol для DOI и библиографии;
- расширить `akademicheskaya-statya`:
  - шаблоны русской и английской аннотации;
  - ГОСТ bibliography checklist;
  - требования ВАК-статьи и диссертационной главы;
  - правила для English manuscript by Russian author;
- расширить `akademicheskii-retsenzent`:
  - отдельный блок для ВАК/диссертационного совета;
  - отдельный блок для international journal review;
  - re-review checklist с traceability table;
- расширить `akademicheskii-konveer`:
  - bilingual entry point detection;
  - language handoff contracts;
  - финальный пакет: RU, EN или bilingual.

Результат:

- русские skills становятся не только переводом, а полноценным локальным академическим слоем.

### Этап 4. Команды и установка

Задачи:

- решить naming convention:
  - оставить upstream `/ars-*` для английского ядра;
  - добавить `/ars-ru-*` для русского контекста;
  - добавить `/ars-auto` или router-документ для auto mode;
- подготовить команды:
  - `/ars-ru-research`;
  - `/ars-ru-paper`;
  - `/ars-ru-reviewer`;
  - `/ars-ru-pipeline`;
- обновить `.claude-plugin/plugin.json` и `.claude-plugin/marketplace.json`, если plugin должен устанавливать оба набора;
- добавить инструкции установки:
  - Claude Code;
  - Opencode;
  - ручная установка только английских skills;
  - ручная установка только русских skills;
  - установка bilingual bundle.

Результат:

- пользователь может явно выбрать English, Russian или auto/bilingual workflow.

### Этап 5. Тесты и evals

Задачи:

- добавить routing tests:
  - русский запрос на обзор литературы -> `akademicheskoe-issledovanie`;
  - English request for paper draft -> `academic-paper`;
  - русский запрос для Scopus/APA -> Russian writing skill with APA output;
  - English request for VAK/GOST -> Russian context skill;
  - mixed RU/EN corpus -> research skill with source language tracking;
- добавить quality fixtures:
  - ГОСТ bibliography examples;
  - fake DOI/source hallucination examples;
  - русские AI-cliche examples;
  - ВАК/РИНЦ review criteria examples;
  - reviewer response traceability examples;
- добавить lightweight lint:
  - русские skills содержат upstream snapshot;
  - русские skills содержат license attribution;
  - skill names в README совпадают с каталогами;
  - routing docs покрывают 4 базовых skill-пары;
  - slash commands не конфликтуют с upstream `/ars-*`.

Результат:

- bilingual behavior можно проверять автоматически;
- изменения в README или skills не ломают маршрутизацию незаметно.

### Этап 6. Документация

Задачи:

- `README.md`: короткий bilingual overview;
- `README.ru.md`: подробная русская инструкция;
- `README.en.md`: английская инструкция для fork users;
- `docs/bilingual-routing.md`: правила выбора языка и skill;
- `docs/russian-academic-context.md`: ГОСТ, ВАК, РИНЦ, eLIBRARY, CyberLeninka, ограничения;
- `docs/upstream-sync.md`: как подтягивать исходный проект и обновлять русские adapters;
- `examples/ru/`: примеры русских запросов и ожидаемых skills;
- `examples/bilingual/`: mixed-language workflows.

Результат:

- проект становится понятным не только автору форка;
- contributors видят, куда добавлять EN/RU изменения.

### Этап 7. Upstream sync workflow

Задачи:

- добавить remote:
  - `origin` -> `dubr1k/academic-research-skills`;
  - `upstream` -> `Imbad0202/academic-research-skills`;
- создать процесс обновления:
  1. fetch upstream;
  2. diff upstream snapshot vs latest;
  3. обновить английское ядро;
  4. проверить `docs/skill-parity-matrix.md`;
  5. перенести релевантные изменения в `russian-academic-skills`;
  6. обновить snapshot hash в русских skills;
  7. прогнать routing/lint tests;
- добавить changelog секции:
  - upstream sync;
  - Russian context changes;
  - bilingual routing changes.

Результат:

- форк можно поддерживать после новых версий исходного проекта без ручного хаоса.

## Приоритеты

### P0

- `README.md` как bilingual landing;
- `README.ru.md` и `README.en.md`;
- `docs/bilingual-routing.md`;
- `docs/skill-parity-matrix.md`;
- routing policy для Claude Code и Opencode.

### P1

- унификация frontmatter русских skills;
- `/ars-ru-*` команды или documented aliases;
- тесты маршрутизации;
- lint на snapshot/license/name consistency.

### P2

- расширение русских references/templates;
- примеры `examples/ru` и `examples/bilingual`;
- plugin metadata для bilingual bundle;
- более глубокие evals качества русских академических выходов.

## Критерии готовности первой версии

Версия bilingual fork считается готовой, если:

- English workflows продолжают использовать upstream skills без регрессий;
- Russian workflows используют `russian-academic-skills`;
- mixed RU/EN workflows имеют описанные правила выбора языка и citation style;
- README дает понятный вход для EN и RU пользователей;
- есть минимум 10 routing fixtures и они проходят;
- все русские skills содержат upstream attribution и snapshot;
- documented update path позволяет подтянуть новую upstream версию и понять, какие русские файлы нужно пересмотреть.

## Риски

- Полная локализация всех upstream agents может привести к дорогой поддержке при каждом upstream update.
- ГОСТ и требования журналов меняются и часто отличаются по редакциям; skill должен явно просить требования конкретного журнала, если нужна финальная точность.
- eLIBRARY/РИНЦ/CyberLeninka не всегда дают надежные метаданные; skill должен различать verified, partially verified и user-provided sources.
- Автоматический language detection может ошибаться на mixed prompts; пользовательский явный выбор должен иметь приоритет.
- Русская адаптация не должна ослаблять upstream integrity gates: запрет на вымышленные источники, claim support и citation verification остаются обязательными.

## Следующий практический шаг

P0, P1, P2, первый P3 depth pass, Post-P3a judged evals, Post-P3b venue examples, Post-P3c upstream sync, Post-P3d candidate-output capture, Post-P3e cached verdict metrics и Post-P3f verdict calibration выполнены. Следующий практический шаг:

1. При следующем upstream release снова выполнить `docs/upstream-sync.md` поверх snapshot `88fc003e6abf5fe9fe86dc8200f8d4aa8d511956`.
