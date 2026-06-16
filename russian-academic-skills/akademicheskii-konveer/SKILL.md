---
name: akademicheskii-konveer
description: "Русскоязычный academic pipeline orchestrator skill для Opencode. Используйте для полного цикла research -> paper -> integrity check -> review -> revision -> re-review -> finalization. Координирует akademicheskoe-issledovanie, akademicheskaya-statya и akademicheskii-retsenzent. Адаптировано из imbad0202/academic-research-skills под русский язык и Opencode task()."
version: "3.12.0-ru.1"
last_updated: "2026-06-16"
status: "active-russian-adapter"
data_access_level: "orchestrates_user_materials_and_verified_sources"
task_type: "pipeline"
depends_on:
  - "akademicheskoe-issledovanie"
  - "akademicheskaya-statya"
  - "akademicheskii-retsenzent"
upstream_snapshot: "175f79bcca4467949fa94e410c25823bd574f687"
upstream_version: "v3.12.0"
upstream_date: "2026-06-08"
---

# Академический конвейер

Русскоязычная адаптация идей `academic-pipeline` из `imbad0202/academic-research-skills` для Opencode. Skill не выполняет всю содержательную работу сам: он определяет стадию, выбирает режим, загружает нужные skills, управляет checkpoint-ами и integrity gates.

Источник адаптации: https://github.com/imbad0202/academic-research-skills
Upstream snapshot: `175f79bcca4467949fa94e410c25823bd574f687` (`v3.12.0`, 2026-06-08).
Лицензия источника: Creative Commons Attribution-NonCommercial 4.0 International, Copyright (c) 2026 Cheng-I Wu.

Локальные материалы:

- `agents/russian_pipeline_state_agent.md` - агент состояния русского/bilingual pipeline и checkpoint handoffs.
- `references/bilingual-handoff-contracts.md` - language state и handoff contracts между стадиями.
- `templates/pipeline-dashboard.md` - dashboard полного русского/bilingual academic pipeline.

## Когда использовать

Используйте skill, если пользователь хочет полный или частичный путь:

- от темы исследования к статье;
- от обзора литературы к рукописи;
- от черновика к рецензии и revision;
- от reviewer comments к revised manuscript и response letter;
- end-to-end workflow для статьи, диссертационной главы, ВАК/РИНЦ публикации.

Русские триггеры: `полный цикл`, `исследование в статью`, `от темы до статьи`, `конвейер статьи`, `научный workflow`, `research to paper`, `paper pipeline`, `подготовить публикацию`, `статья с нуля`, `провести через рецензию`, `доработать после рецензии`.

Не используйте конвейер, если пользователь просит только один шаг: только поиск литературы, только аннотацию, только citation-check или только рецензию. В таком случае загрузите соответствующий sub-skill напрямую.

## Подчиненные skills

- `akademicheskoe-issledovanie`: research, literature review, fact-check, systematic review.
- `akademicheskaya-statya`: planning, drafting, citation, revision, formatting.
- `akademicheskii-retsenzent`: multi-perspective review, methodology review, re-review.

## Главный принцип

Оркестратор не пишет статью, не делает исследование и не рецензирует сам. Он:

1. определяет entry point;
2. рекомендует режим;
3. запускает нужные skills/tasks;
4. проверяет наличие deliverables;
5. показывает checkpoint;
6. передает материалы следующей стадии.

## Entry point detection

Определите, что уже есть у пользователя:

| Материалы | Стартовая стадия |
|---|---|
| Только тема или интерес | Stage 1 Research |
| Есть RQ и источники | Stage 2 Write или Stage 1 lit-review gap-fill |
| Есть черновик статьи | Stage 2.5 Integrity |
| Есть проверенный черновик | Stage 3 Review |
| Есть reviewer comments | Stage 4 Revise |
| Есть revised manuscript + response | Stage 3' Re-review |
| Есть финальный текст | Stage 4.5 Final Integrity или Stage 5 Finalize |

Если entry point неясен, задайте один вопрос: `Какие материалы уже есть: тема, список источников, черновик, замечания рецензентов или финальный текст?`

## 10 стадий

| Stage | Название | Skill/режим | Deliverable |
|---|---|---|---|
| 1 | Research | `akademicheskoe-issledovanie`: socratic/full/quick/lit-review | RQ, methodology, bibliography, synthesis |
| 2 | Write | `akademicheskaya-statya`: plan/full | paper blueprint или draft |
| 2.5 | Integrity | claim/citation/data verification | integrity report + fixes needed |
| 3 | Review | `akademicheskii-retsenzent`: full | review reports + decision + roadmap |
| 4 | Revise | `akademicheskaya-statya`: revision | revised draft + response to reviewers |
| 3' | Re-review | `akademicheskii-retsenzent`: re-review | verification review |
| 4' | Re-revise | `akademicheskaya-statya`: revision | second revised draft |
| 4.5 | Final Integrity | full claim/citation check | final verification report |
| 5 | Finalize | `akademicheskaya-statya`: format-convert/disclosure | final package |
| 6 | Process Summary | orchestrator | process record and AI disclosure summary |

## State machine

1. Stage 1 -> user confirmation -> Stage 2.
2. Stage 2 -> user confirmation -> Stage 2.5.
3. Stage 2.5 PASS -> Stage 3; FAIL -> fix and re-verify, max 3 rounds.
4. Stage 3 Accept -> Stage 4.5; Minor/Major -> Stage 4; Reject -> Stage 2 restructure or stop.
5. Stage 4 -> user confirmation -> Stage 3'.
6. Stage 3' Accept/Minor -> Stage 4.5; Major -> Stage 4'.
7. Stage 4' -> user confirmation -> Stage 4.5, no second full review loop by default.
8. Stage 4.5 PASS with zero blocking issues -> Stage 5; FAIL -> fix and re-verify.
9. Stage 5 -> content confirmation -> final package.
10. Stage 6 -> process summary -> end.

## Checkpoints

После каждой стадии показывайте checkpoint и ждите пользователя, если переход меняет содержание работы.

Типы checkpoint:

- FULL: первый checkpoint, integrity boundaries, before finalization.
- SLIM: короткий статус после нескольких `продолжай`.
- MANDATORY: integrity FAIL, review decision, finalization.

Шаблон:

```text
Stage [N] [Name] complete
Deliverables:
- ...
Quality/integrity flags:
- ...
Recommended next stage: ...
Options:
1. Continue
2. Review deliverables
3. Adjust scope/mode
4. Pause
```

Нельзя auto-skip MANDATORY checkpoints.

## Integrity gates

Stage 2.5 и 4.5 обязательны. Они проверяют:

1. Reference existence: источник существует.
2. Citation consistency: in-text citations и bibliography совпадают.
3. Claim support: claim действительно поддержан источником.
4. Numerical accuracy: числа, проценты, p-values, sample sizes совпадают.
5. Data/method consistency: выводы не превышают данные.
6. Originality/plagiarism risk: нет неатрибутированных заимствований.
7. AI research failure modes: hallucinated sources, fabricated methods/results, shortcut reliance, bug-as-insight, overclaiming.

Вердикты:

- PASS: zero blocking issues;
- PASS_WITH_NOTES: только minor notes или inaccessible-but-existing sources;
- FAIL: fabricated source, unsupported claim, major distortion, methodology fabrication, untraceable data.

Stage 4.5 проверяет с нуля, а не только старые проблемы.

## Handoff contracts

### Stage 1 -> Stage 2

Передайте:

- Research Question Brief;
- Methodology Blueprint;
- Annotated Bibliography;
- Synthesis Report;
- ограничения и unresolved controversies.

### Stage 2 -> Stage 2.5

Передайте:

- полный draft;
- bibliography;
- figures/tables/data notes;
- список claims, если уже есть.

### Stage 3 -> Stage 4

Передайте:

- Editorial Decision;
- Review Reports;
- Revision Roadmap;
- обязательные и optional правки.

### Stage 4 -> Stage 3'

Передайте:

- revised manuscript;
- response to reviewers;
- traceability table.

### Stage 4.5 -> Stage 5

Передайте:

- verified final draft;
- final bibliography;
- disclosure/funding/COI/ethics statements;
- требования формата.

## Opencode execution pattern

Загружайте sub-skills перед делегацией:

```text
skill(name="akademicheskoe-issledovanie")
skill(name="akademicheskaya-statya")
skill(name="akademicheskii-retsenzent")
```

Параллелизация:

- В Stage 1 можно параллельно запускать bibliography search, source verification и devil's advocate search.
- В Stage 2 после outline можно параллельно готовить literature matrix, figures/tables и argument blueprint.
- В Stage 3 reviewers должны работать независимо и параллельно.
- Integrity gates запускайте после получения полного текста, не параллельно с его написанием.

Категории:

```text
research synthesis: task(category="deep")
methodology hard reasoning: task(category="ultrabrain")
writing/revision: task(category="writing")
review panel: task(category="ultrabrain"/"writing"/"deep"/"artistry") by perspective
external sources: task(subagent_type="librarian", run_in_background=true)
local corpus search: task(subagent_type="explore", run_in_background=true)
```

## User mode recommendation

Перед запуском предложите режим:

| Пользователь | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|
| Не знает тему | socratic | plan | guided |
| Опытный, хочет результат | full | full | full |
| Мало времени | quick | outline/full | quick |
| Есть статья | skip/backfill | skip | full after integrity |
| Есть review comments | skip | revision | re-review |

## Progress dashboard

```text
Academic Pipeline Status
[1] Research        DONE/PENDING
[2] Write           DONE/PENDING
[2.5] Integrity     PASS/FAIL/PENDING
[3] Review          DONE/PENDING
[4] Revise          DONE/PENDING
[3'] Re-review      DONE/PENDING
[4'] Re-revise      DONE/PENDING
[4.5] Final check   PASS/FAIL/PENDING
[5] Finalize        DONE/PENDING
[6] Process summary DONE/PENDING
Current stage: ...
Blocking issues: ...
Next action: ...
```

## Process summary

В конце подготовьте краткий process record:

- исходная цель;
- какие stages выполнены;
- какие источники и материалы использованы;
- какие integrity checks пройдены;
- какие решения принимал пользователь;
- где применялся AI;
- ограничения результата;
- что нужно проверить вручную перед отправкой в журнал/ВАК.

## Анти-паттерны

- Оркестратор сам пишет содержательные разделы.
- Пропуск Stage 2.5 или 4.5, потому что `текст выглядит нормально`.
- Автоматический переход после review decision без пользователя.
- Потеря reviewer concerns при revision.
- Проверка только старых ошибок на final integrity.
- Слишком много revision loops без улучшения качества.
- Превращение advisory collaboration notes в блокирующие условия.
- Выдумывание источников для заполнения bibliography gaps.

## Минимальный стартовый ответ

Когда skill активирован, начните так:

```text
Определяю entry point. Какие материалы уже есть: только тема, список источников, черновик статьи, замечания рецензентов или revised manuscript?
```

Если entry point очевиден, не спрашивайте лишнего: назовите стадию, режим и следующий checkpoint.
