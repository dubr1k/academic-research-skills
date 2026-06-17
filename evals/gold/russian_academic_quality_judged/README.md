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

Run with:

```bash
python -m scripts.check_russian_academic_quality_judged
python -m scripts.run_evals --task russian_academic_quality_judged
pytest scripts/test_check_russian_academic_quality_judged.py tests/test_russian_academic_evals.py
```
