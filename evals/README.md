# evals/ — gold-set corpora for ARS measurement targets

This directory holds the v3.10 #184 generalized gold sets. Each subdirectory under `gold/` is a self-contained gold set for one measurement target. The structure mirrors the v3.8 `scripts/fixtures/claim_audit_calibration/` pattern but generalizes to multiple targets.

## Layout

```
evals/
├── README.md                          # this file
├── gold/
│   ├── citation_extraction/           # Phase 1a/1b — baseline for #182
│   │   ├── README.md
│   │   ├── manifest.yaml
│   │   ├── tuples/
│   │   │   └── NNN-{kind-slug}-{discriminator}.json
│   │   └── expected_outcomes.json
│   ├── rq_framing_patterns/           # #257 Socratic wording advisory calibration
│   ├── russian_academic_quality/      # Russian ГОСТ/ВАК/РИНЦ advisory calibration
│   ├── russian_academic_quality_judged/# Russian recorded-output judged eval
│   ├── status_classification/         # Phase 2 (lands post-#183)
│   └── summarization_adequacy/        # Phase 2 (lands post-#183)
```

## Running the harness (#184 Phase 1b)

The multi-task harness `scripts/run_evals.py` discovers every `gold/<task>/manifest.yaml`, measures each task, and emits a report shaped by `shared/evals_lift_report.schema.json`:

```
PYTHONPATH=. python -m scripts.run_evals                          # all tasks
PYTHONPATH=. python -m scripts.run_evals --task citation_extraction --output report.json
PYTHONPATH=. python -m scripts.run_evals --baseline before.json --compare after.json
```

`--baseline` + `--compare` produce a side-by-side report (`lift_pre` / `lift_post`). The ranking-lift gate `scripts/check_ranking_lift.py` reads those reports and blocks on un-acknowledged regressions; CI wires both via `.github/workflows/eval-harness.yml` (Delta 3 path filter). Tasks whose entrypoint module or gold set is not yet present are reported as `pending`/`skipped` rather than failing.

## Authoring conventions

See each task's `README.md` for task-specific conventions (tuple naming, kind distributions, expected outcomes shape).

## Validator

Run `python -m scripts.check_evals_gold_set evals/gold/citation_extraction` for the citation tuple/expected-outcome format. Gold sets that use a native `gold_set.json` checker, such as the Russian academic quality tasks, should be validated through their task-specific `scripts.check_*` module and `scripts.run_evals.py`.

## Provenance

- Phase 1a (citation-extraction gold set) + Phase 1b (`run_evals.py` harness + lift gate): v3.10 #184, spec `docs/design/2026-05-21-v3.10-184-extend-eval-harness-spec.md`
- RQ framing patterns: Kong #257 idea-diversity advisory, spec `docs/design/2026-05-28-kong-257-idea-diversity-coverage-gap-advisory.md`
- Russian academic quality: bilingual fork P2e/P2f advisory calibration and structural measurer for ГОСТ, ВАК/РИНЦ, eLIBRARY/CyberLeninka source verification, Russian style, revision traceability, and mixed-language routing.
- Russian academic quality judged: Post-P3 recorded-output judged layer for the same Russian labels. CI scores cached `model_output` text deterministically against rubric markers; live LLM judging remains a future advisory layer.
- Phase 2 (status + summarization): scheduled post-#183 ship
