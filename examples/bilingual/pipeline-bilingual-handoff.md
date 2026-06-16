# Bilingual Example: Pipeline Handoff With Russian Sources And English Output

Request:

```text
На русском проведи полный pipeline: сначала проверь русские и англоязычные источники по цифровой педагогике, потом подготовь статью на английском для Scopus, проведи рецензию, revision и финальный bilingual package с русской матрицей источников.
```

Expected skill: `akademicheskii-konveer`

Routing:

- Interaction language: Russian.
- `output_language: en` for the manuscript.
- `source_language: [ru, en]` for the mixed corpus.
- `final_package_mode: bilingual` because the package includes an English manuscript plus Russian-facing source matrix/verification notes.
- Research routes through `akademicheskoe-issledovanie`, writing/revision through `akademicheskaya-statya`, review/re-review through `akademicheskii-retsenzent`.

Expected handoff state:

```yaml
pipeline_state:
  current_stage: "1"
  interaction_language: ru
  output_language: en
  source_language: [ru, en]
  venue_context: scopus
  citation_style: apa
  final_package_mode: bilingual
  source_verification_state:
    status: in_progress
    per_source:
      - source_id: RU-01
        source_language: ru
        source_system: elibrary
        verification_status: partially_verified
        metadata_missing: [pages]
        supports_claims: limited
        unresolved_risks: [rinc_indexing_needs_current_check]
      - source_id: EN-01
        source_language: en
        source_system: doi
        verification_status: verified_current
        metadata_missing: []
        supports_claims: yes
        unresolved_risks: []
    aggregate:
      verified_count: 1
      partial_count: 1
      rejected_count: 0
      unresolved_risks: [rinc_indexing_needs_current_check]
    last_gate: none
    carryover_required: true
  gate_carryover:
    stage_2_5: pending
    stage_4_5: pending
    blocking_issues: []
    open_reviewer_concerns: []
  checkpoint_carryover:
    checkpoint_type: full
    user_decision_required: true
    allowed_next_stage: "Stage 2 Writing after research confirmation"
```

Expected checks:

- Research -> Writing handoff includes `source_verification_state`, `output_language`, `source_language`, and `final_package_mode`.
- Writing -> Integrity handoff keeps Russian source titles in original form and marks any writing-stage source additions as `not_verified`.
- Stage 2.5 fails if fabricated sources, unsupported claims, or untraceable data appear in the English manuscript.
- Review -> Revision handoff carries reviewer concern IDs and unresolved source risks.
- Revision -> Re-review handoff updates changed claims/citations/source additions before closure.
- Final Integrity -> Finalization handoff produces `final_package_mode: bilingual` with English manuscript files and a Russian/English source verification matrix.
- Shared/global agents receive the Russian venue/source context before delegation and are audited for English international defaults.

Expected final package:

- English manuscript formatted for the target international venue.
- APA or journal-specific references with original Russian titles preserved where required.
- Russian-facing source verification matrix with eLIBRARY/РИНЦ/ВАК/CyberLeninka distinctions.
- Integrity reports from Stage 2.5 and Stage 4.5.
- Review/revision traceability table with open concerns closed or explicitly carried forward.
