---
name: akademicheskii-konveer
description: "Русскоязычный academic pipeline orchestrator skill для Opencode. Используйте для полного цикла research -> paper -> integrity check -> review -> revision -> re-review -> finalization. Координирует akademicheskoe-issledovanie, akademicheskaya-statya и akademicheskii-retsenzent. Адаптировано из imbad0202/academic-research-skills под русский язык и Opencode task()."
version: "3.15.0-ru.1"
last_updated: "2026-07-10"
status: "active-russian-adapter"
data_access_level: "orchestrates_user_materials_and_verified_sources"
task_type: "pipeline"
depends_on:
  - "akademicheskoe-issledovanie"
  - "akademicheskaya-statya"
  - "akademicheskii-retsenzent"
upstream_snapshot: "ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c"
upstream_version: "v3.15.0"
upstream_date: "2026-07-08"
---

# Академический конвейер

Русскоязычная адаптация идей `academic-pipeline` из `imbad0202/academic-research-skills` для Opencode. Skill не выполняет всю содержательную работу сам: он определяет стадию, выбирает режим, загружает нужные skills, управляет checkpoint-ами, integrity gates и bilingual handoff state.

Источник адаптации: https://github.com/imbad0202/academic-research-skills
Upstream snapshot: `ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c` (`v3.15.0`, 2026-07-08).
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
6. передает материалы следующей стадии;
7. сохраняет `source_verification_state`, `output_language`, `source_language`, `final_package_mode` и checkpoint/gate carryover между research, writing, review и revision.

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

### Runtime enforcement state (v3.15)

В hook-enabled Claude Code deterministic write-scope guard ограничивает single-phase agents. На Windows launcher использует Git Bash и рабочий Python; если Python отсутствует, optional guard cleanly no-op. Оркестратор обязан явно записать `write_scope_guard: active|inactive|unsupported` в runtime state, но не должен считать inactive guard integrity failure: обязательные Stage 2.5/4.5, handoff contracts и post-task diff checks остаются в силе во всех runtimes.

Для Opencode/Codex передавайте allowlist artifacts в каждом `task()` и проверяйте, что агент не изменил чужую фазу. Ambiguous cross-phase materials должны попасть в clarification до делегации, а не в автоматический multi-phase run.

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

## Bilingual pipeline state

Каждый stage handoff должен нести явный state object. Не смешивайте язык общения, язык источников и язык финального текста.

```yaml
pipeline_state:
  current_stage: "1|2|2.5|3|4|3'|4'|4.5|5|6"
  output_language: "ru|en|bilingual"
  source_language: ["ru", "en"]
  interaction_language: "ru|en|mixed"
  venue_context: "vak|rinc|elibrary|scopus|wos|dissertation_council|journal_specific|mixed"
  citation_style: "gost|apa|ieee|vancouver|journal_override"
  final_package_mode: "RU|EN|bilingual"
  source_verification_state:
    status: "not_started|in_progress|partial|pass|pass_with_notes|fail"
    per_source:
      - source_id: ""
        source_language: "ru|en|other"
        source_system: "elibrary|rinc|vak|cyberleninka|doi|scopus|wos|publisher|archive|other"
        verification_status: "verified_current|partially_verified|not_verified|inaccessible|rejected"
        metadata_missing: []
        supports_claims: "yes|limited|no"
        unresolved_risks: []
    aggregate:
      verified_count: 0
      partial_count: 0
      rejected_count: 0
      unresolved_risks: []
    last_gate: "none|stage_2_5|stage_4_5"
    carryover_required: true
  gate_carryover:
    stage_2_5: "pending|pass|pass_with_notes|fail"
    stage_4_5: "pending|pass|pass_with_notes|fail"
    blocking_issues: []
    open_reviewer_concerns: []
  checkpoint_carryover:
    last_checkpoint: "entry|stage_complete|integrity_fail|review_decision|finalization"
    user_decision_required: true
    allowed_next_stage: ""
```

Обязательные правила:

- `output_language` описывает язык рукописи/deliverables, `source_language` описывает язык корпуса источников.
- `final_package_mode` фиксируется до Stage 5: `RU`, `EN` или `bilingual`.
- `source_verification_state` переносится из Stage 1 в Stage 2, затем обновляется на Stage 2.5 и Stage 4.5.
- `gate_carryover.blocking_issues` нельзя очищать без evidence из текста, bibliography или verification report.
- При bilingual режиме сохраняйте оригинальные названия русских источников; перевод можно добавить отдельным полем, но не заменять оригинал.

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

Checkpoint всегда должен показывать carryover:

```text
Language state:
- output_language:
- source_language:
- final_package_mode:
Source verification state:
- status:
- unresolved_risks:
Gate carryover:
- stage_2_5:
- stage_4_5:
- blocking_issues:
```

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
- `pipeline_state` с `output_language`, `source_language`, `final_package_mode`;
- `source_verification_state` по каждому источнику и агрегированный статус.

### Stage 2 -> Stage 2.5

Передайте:

- полный draft;
- bibliography;
- figures/tables/data notes;
- список claims, если уже есть.
- `source_verification_state` из Stage 1 без потери unresolved risks;
- `checkpoint_carryover` с подтверждением пользователя на integrity gate.

### Stage 3 -> Stage 4

Передайте:

- Editorial Decision;
- Review Reports;
- Revision Roadmap;
- обязательные и optional правки.
- `gate_carryover` из Stage 2.5;
- reviewer concern IDs, которые должны сохраниться в revision traceability table.

### Stage 4 -> Stage 3'

Передайте:

- revised manuscript;
- response to reviewers;
- traceability table.
- `source_verification_state` после изменений в claims/bibliography;
- open reviewer concerns и evidence для закрытых concerns.

### Stage 4.5 -> Stage 5

Передайте:

- verified final draft;
- final bibliography;
- disclosure/funding/COI/ethics statements;
- требования формата.
- `final_package_mode: RU|EN|bilingual`;
- final `source_verification_state` и remaining manual checks.

Подробный contract: `references/bilingual-handoff-contracts.md`.

## Global/shared agent audit before delegation

Если русский adapter вызывает shared/global agents, не предполагайте, что они автоматически понимают ВАК, РИНЦ, eLIBRARY, ГОСТ или российские журнальные нормы. Перед вызовом проверьте и явно передайте:

- `interaction_language`, `output_language`, `source_language`, `final_package_mode`;
- российский venue/context: ВАК, РИНЦ, eLIBRARY, диссертационный совет, конкретный журнал;
- citation style и journal override, если ГОСТ не является целью;
- запрет silently translate Russian titles или заменять ГОСТ/ВАК требования English international defaults;
- source verification distinctions: CyberLeninka as access channel, eLIBRARY record, РИНЦ indexing, ВАК status, DOI, peer-review evidence;
- gate policy: Stage 2.5 и Stage 4.5 обязательны, unresolved source risks carry over;
- expected output package: RU-only, EN-only, or bilingual with separate Russian originals and English-facing elements.

Если shared/global agent возвращает English-centric defaults, оркестратор должен отметить это как `global_agent_norm_risk` и запросить correction before stage completion.

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
