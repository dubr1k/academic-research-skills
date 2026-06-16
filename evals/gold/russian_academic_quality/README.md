# Russian Academic Quality Gold Set

This gold set captures Russian academic quality risks that the bilingual adapter layer must handle consistently. It is an advisory-calibration set, not a deterministic runtime harness.

## Scope

- ГОСТ bibliography checks, including ГОСТ Р 7.0.5-2008 metadata gaps, source-type patterns, and journal override handling.
- ВАК/РИНЦ separation, including eLIBRARY presence that does not prove ВАК status.
- Source verification for DOI, eLIBRARY, РИНЦ/ВАК status claims, CyberLeninka access copies, incomplete Russian records, and mixed RU/EN corpora.
- Russian academic style checks for vague relevance statements and AI-like cliches.
- Revision-response traceability for reviewer replies and manuscript locations.
- Mixed-language routing where source_language and output-language requirements must be preserved.

## Labels

- `gost_bibliography`: bibliography metadata, source-type classification, journal override, and ГОСТ formatting risks.
- `vak_rinc_status`: ВАК/РИНЦ/eLIBRARY status classification risks.
- `source_verification`: DOI, current status evidence, metadata gaps, access-channel, and source-language verification risks.
- `russian_style`: Russian academic style and cliche risks.
- `revision_traceability`: reviewer-response traceability risks.
- `mixed_language_routing`: RU/EN routing and source-language preservation risks.

## Expected Use

The expected guards describe what a Russian skill or bilingual router must surface. The `must_not_do` field records forbidden behavior, especially guessing missing metadata, forcing ГОСТ when a journal override requires APA/IEEE/Vancouver/Chicago, treating РИНЦ as ВАК, fabricating DOI values, silently translating source titles, or marking reviewer comments addressed without manuscript evidence.

Run the structural tests with:

```bash
python -m scripts.check_russian_academic_quality
python -m scripts.run_evals --task russian_academic_quality
pytest tests/test_russian_academic_evals.py scripts/test_check_russian_academic_quality.py
```
