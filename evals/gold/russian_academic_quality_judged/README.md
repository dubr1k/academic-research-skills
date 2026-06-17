# Russian Academic Quality Judged Output Gold Set

This gold set is the first LLM-output judged layer for the Russian academic
adapter. It complements `russian_academic_quality`, which checks that prompts
and expected guards are structurally gradeable.

## Scope

- Recorded `model_output` examples for ГОСТ bibliography, ВАК/РИНЦ status
  separation, source verification, Russian academic style, revision
  traceability, and mixed-language routing.
- Rubric-level `must_include` markers that a good model answer must surface.
- Rubric-level `must_avoid` markers for critical failures such as fabricated
  DOI values, collapsing ВАК/РИНЦ/eLIBRARY distinctions, silently translating
  titles, or closing reviewer concerns without manuscript evidence.

## Metrics

- `judged_pass_rate`: share of recorded outputs that include all required
  markers, no forbidden markers, and cached judge verdicts marked `pass`.
- `critical_failure_rate`: share of recorded outputs that contain forbidden
  output markers.
- `dimension_pass_rate`: share of cached judge dimensions marked `pass`.
- `needs_human_review_rate`: share of cases whose cached verdict or dimensions
  require human review.

## Candidate Output Capture

The canonical recorded outputs remain in `gold_set.json` as `model_output`
fields. The sibling `candidate_outputs/baseline/` directory mirrors each output
as a standalone Markdown file plus `manifest.json` with SHA-256 hashes. This
keeps the current deterministic checker simple while giving future live/cached
LLM judges stable files to consume.

## Cached Judge Verdicts

The `judge_verdicts/baseline/` directory stores deterministic cached verdicts
for each captured candidate output. Each verdict records:

- `verdict`: `pass`, `fail`, or `needs_human_review`;
- `dimension_results`: per-dimension `pass`, `fail`, or `needs_human_review`;
- `hard_failures`;
- `candidate_path` and `candidate_sha256` pinned to the capture manifest;
- short rationale and evidence quotes.

`needs_human_review` is deliberately not a pass. This keeps future live/cached
judge integration conservative while preserving deterministic CI behavior.

Regenerate or verify the capture with:

```bash
python -m scripts.capture_russian_academic_quality_outputs
python -m scripts.capture_russian_academic_quality_outputs --check
```

Run with:

```bash
python -m scripts.capture_russian_academic_quality_outputs --check
python -m scripts.check_russian_academic_quality_judged --verdict-dir evals/gold/russian_academic_quality_judged/judge_verdicts/baseline
python -m scripts.run_evals --task russian_academic_quality_judged
pytest scripts/test_capture_russian_academic_quality_outputs.py scripts/test_check_russian_academic_quality_judged.py tests/test_russian_academic_evals.py
```
