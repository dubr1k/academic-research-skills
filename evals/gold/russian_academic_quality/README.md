# Russian Academic Quality Gold Set

This gold set captures Russian academic quality risks that the bilingual adapter layer must handle consistently. It is an advisory-calibration set, not a deterministic runtime harness.

## Scope

- ГОСТ bibliography checks, including ГОСТ Р 7.0.5-2008 metadata gaps.
- ВАК/РИНЦ separation, including eLIBRARY presence that does not prove ВАК status.
- Source verification for DOI, eLIBRARY, CyberLeninka, and user-provided bibliographic claims.
- Russian academic style checks for vague relevance statements and AI-like cliches.
- Revision-response traceability for reviewer replies and manuscript locations.
- Mixed-language routing where source_language and output-language requirements must be preserved.

## Labels

- `gost_bibliography`: bibliography metadata and ГОСТ formatting risks.
- `vak_rinc_status`: ВАК/РИНЦ/eLIBRARY status classification risks.
- `source_verification`: DOI and source-existence verification risks.
- `russian_style`: Russian academic style and cliche risks.
- `revision_traceability`: reviewer-response traceability risks.
- `mixed_language_routing`: RU/EN routing and source-language preservation risks.

## Expected Use

The expected guards describe what a Russian skill or bilingual router must surface. The `must_not_do` field records forbidden behavior, especially guessing missing metadata, treating РИНЦ as ВАК, fabricating DOI values, silently translating source titles, or marking reviewer comments addressed without manuscript evidence.

Run the structural tests with:

```bash
pytest tests/test_russian_academic_evals.py
```
