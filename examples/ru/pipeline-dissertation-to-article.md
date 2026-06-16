# RU Pipeline Example: Dissertation Chapter To Article

Request:

```text
Проведи полный цикл: из главы диссертации сделать статью для российского журнала, проверить источники, отрецензировать и подготовить финальный пакет.
```

Expected skill: `akademicheskii-konveer`

Routing:

- Full Russian research-to-publication workflow.
- Start from provided dissertation chapter, then route through integrity, review, revision, final check, and formatting.
- `output_language: ru`.
- `source_language: [ru, en]` if the dissertation chapter uses both Russian and international sources.
- `final_package_mode: RU` unless the target journal requests bilingual metadata or English-language files.
- Carry `source_verification_state` from research/backfill into writing, Stage 2.5, review, revision, Stage 4.5, and finalization.

Expected checks:

- detect entry point from available materials;
- preserve language handoff contracts between research, writing, review, and revision;
- require Stage 2.5 and Stage 4.5 integrity checks;
- final package identifies RU, EN, or bilingual components.
- keep `output_language` separate from `source_language`;
- classify every source as `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, or `rejected`;
- preserve unresolved DOI, pages, issue, ВАК/РИНЦ/eLIBRARY status, or claim-support risks as carryover until evidence clears them;
- show checkpoint/gate carryover after Stage 2.5, Stage 3, Stage 4, and Stage 4.5;
- before shared/global agents are called, audit that they received Russian venue/context and did not replace ГОСТ/ВАК/РИНЦ/eLIBRARY assumptions with English international defaults.

Expected pipeline state excerpt:

```yaml
pipeline_state:
  output_language: ru
  source_language: [ru, en]
  final_package_mode: RU
  source_verification_state:
    status: partial
    per_source:
      - source_id: RU-DISS-01
        source_language: ru
        source_system: archive
        verification_status: partially_verified
        metadata_missing: [pages]
        supports_claims: limited
        unresolved_risks: [missing_pages_for_dissertation_source]
      - source_id: RU-JOURNAL-01
        source_language: ru
        source_system: vak
        verification_status: partially_verified
        metadata_missing: [current_vak_status]
        supports_claims: yes
        unresolved_risks: [journal_vak_status_needs_current_check]
    aggregate:
      verified_count: 0
      partial_count: 2
      rejected_count: 0
      unresolved_risks:
        - missing_pages_for_dissertation_source
        - journal_vak_status_needs_current_check
    last_gate: none
    carryover_required: true
  gate_carryover:
    stage_2_5: pending
    stage_4_5: pending
    blocking_issues: []
    open_reviewer_concerns: []
  checkpoint_carryover:
    user_decision_required: true
    allowed_next_stage: "Stage 2.5 Integrity after draft extraction"
```

Expected final package modes:

- `RU`: Russian manuscript, ГОСТ or journal-specific bibliography, Russian disclosures, submission checklist.
- `bilingual`: Russian manuscript plus English title/abstract/keywords or cover materials if the journal requires them.
- `EN`: only if the user changes venue/output target to an English-language journal.
