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
  markers and no forbidden markers.
- `critical_failure_rate`: share of recorded outputs that contain forbidden
  output markers.

## Candidate Output Capture

The canonical recorded outputs remain in `gold_set.json` as `model_output`
fields. The sibling `candidate_outputs/baseline/` directory mirrors each output
as a standalone Markdown file plus `manifest.json` with SHA-256 hashes. This
keeps the current deterministic checker simple while giving future live/cached
LLM judges stable files to consume.

Regenerate or verify the capture with:

```bash
python -m scripts.capture_russian_academic_quality_outputs
python -m scripts.capture_russian_academic_quality_outputs --check
```

Run with:

```bash
python -m scripts.capture_russian_academic_quality_outputs --check
python -m scripts.check_russian_academic_quality_judged
python -m scripts.run_evals --task russian_academic_quality_judged
pytest scripts/test_capture_russian_academic_quality_outputs.py scripts/test_check_russian_academic_quality_judged.py tests/test_russian_academic_evals.py
```
