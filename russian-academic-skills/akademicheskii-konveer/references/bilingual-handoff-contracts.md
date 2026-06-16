# Bilingual Handoff Contracts

Use these contracts when the pipeline crosses research, writing, review, revision, and finalization.

## Language State

Track at every stage:

- interaction language;
- output language;
- source language;
- venue language;
- citation style;
- source corpus languages;
- required RU, EN, or bilingual deliverables;
- final package mode: `RU`, `EN`, or `bilingual`.

Required machine-readable labels:

```yaml
interaction_language: "ru|en|mixed"
output_language: "ru|en|bilingual"
source_language: ["ru", "en"]
venue_language: "ru|en|mixed"
citation_style: "gost|apa|ieee|vancouver|journal_override"
final_package_mode: "RU|EN|bilingual"
```

Never infer `output_language` from `source_language`. A Russian adapter can produce an English article from Russian sources, a Russian article from English sources, or a bilingual package with separate Russian and English deliverables.

## Source Verification State

Carry this object across every handoff:

```yaml
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
```

Carryover rules:

- Stage 1 creates or updates the first source verification state.
- Stage 2 must receive the state before drafting claims.
- Stage 2.5 updates `last_gate: stage_2_5` and cannot erase unresolved risks without evidence.
- Stage 3 receives unresolved source risks so reviewers can distinguish content issues from evidence issues.
- Stage 4 must update the state when claims, citations, bibliography, tables, or source scope change.
- Stage 4.5 updates `last_gate: stage_4_5` and blocks finalization on fabricated sources, unsupported claims, or untraceable data.

## Gate And Checkpoint Carryover

Each checkpoint must include:

```yaml
gate_carryover:
  stage_2_5: "pending|pass|pass_with_notes|fail"
  stage_4_5: "pending|pass|pass_with_notes|fail"
  blocking_issues: []
  open_reviewer_concerns: []
checkpoint_carryover:
  checkpoint_type: "full|slim|mandatory"
  last_checkpoint: "entry|stage_complete|integrity_fail|review_decision|finalization"
  user_decision_required: true
  allowed_next_stage: ""
```

Do not mark `user_decision_required: false` for review decisions, integrity failures, finalization choices, or any transition that changes content.

## Stage Handoffs

### Research -> Writing

Deliver:

- research question;
- methodology blueprint;
- literature matrix with `source_language`, `source_system`, and `verification_status`;
- verified bibliography draft;
- unresolved source risks.
- language state with `output_language`, `source_language`, and `final_package_mode`;
- source verification state;
- checkpoint carryover from research confirmation.

Minimum acceptance:

- every source row has `source_id`, `source_language`, `source_system`, `verification_status`, and `supports_claims`;
- Russian titles remain in original form unless a separate translation field is explicitly added;
- `not_verified`, `partially_verified`, and `inaccessible` records remain visible to the writing stage.

### Writing -> Integrity

Deliver:

- draft sections;
- claim list;
- bibliography;
- tables/figures/data notes;
- disclosure/funding/COI/ethics draft statements.
- unchanged source verification state from research plus any writing-stage source additions;
- output language and final package mode for integrity reporting.

Minimum acceptance:

- every claim that relies on literature links to one or more source IDs;
- bibliography entries preserve original language metadata;
- any new source introduced during writing is `not_verified` until checked.

### Integrity -> Review

Deliver:

- Stage 2.5 integrity verdict: `pass`, `pass_with_notes`, or `fail`;
- issue list with blocking/minor severity;
- updated source verification state;
- unresolved source risks and evidence limitations;
- checkpoint decision that authorizes review only after acceptable gate status.

Minimum acceptance:

- `fail` cannot route to Stage 3 without a fix-and-reverify loop;
- `pass_with_notes` carries notes into review and revision instead of dropping them.

### Review -> Revision

Deliver:

- decision;
- issue list with severity and location;
- required fixes;
- optional improvements;
- reviewer response traceability table.
- source verification state and gate carryover from Stage 2.5;
- output language and final package mode so reviewer requests do not silently change the publication target.

Minimum acceptance:

- each reviewer concern has a stable concern ID;
- revision work keeps concern IDs until re-review closes or reopens them;
- source-related reviewer concerns link back to source IDs or verification risks.

### Revision -> Re-review

Deliver:

- revised manuscript;
- response to reviewers;
- traceability table by concern ID;
- changed claims/citations/source additions;
- updated source verification state;
- open reviewer concerns.

Minimum acceptance:

- closed concerns cite manuscript locations or response evidence;
- new claims or sources introduced during revision are marked for final integrity;
- unresolved source risks carry into Stage 4.5 even if reviewers accept the revision.

### Final Integrity -> Finalization

Deliver:

- verified final manuscript;
- final bibliography;
- final language/citation style declaration;
- remaining manual checks for journal or dissertation council.
- final source verification state;
- final package mode: `RU`, `EN`, or `bilingual`;
- output file/package checklist.

Minimum acceptance:

- `final_package_mode: RU` includes Russian-facing manuscript, bibliography style, disclosures, and journal/council checks;
- `final_package_mode: EN` includes English-facing manuscript, citation style, disclosures, and international venue checks while preserving source-language metadata;
- `final_package_mode: bilingual` includes both language-facing deliverables and a source matrix that preserves original titles.

## Shared/Global Agent Audit

Russian adapters may call shared/global agents, but the handoff must prevent accidental English international defaults.
Stable marker: shared agent context audit must be recorded before and after delegation.

Before delegation, inspect and pass:

- `interaction_language`, `output_language`, `source_language`, `final_package_mode`;
- venue/context: ВАК, РИНЦ, eLIBRARY, CyberLeninka, dissertation council, Scopus/WoS, journal-specific override;
- citation rules: ГОСТ, APA, IEEE, Vancouver, or journal override;
- source verification distinctions: access channel vs index status vs peer-review evidence vs claim support;
- required handling of Russian titles, transliteration, translated titles, and bilingual references;
- integrity gate policy and unresolved risks.

After delegation, audit:

- Did the agent assume APA/Scopus/English norms because the task is academic?
- Did it replace ГОСТ, ВАК, РИНЦ, eLIBRARY, or Russian journal constraints with international defaults?
- Did it silently translate source titles or merge distinct Russian records?
- Did it treat CyberLeninka access, DOI presence, or index presence as claim support?
- Did it drop `source_verification_state`, `gate_carryover`, or `final_package_mode`?

If yes, mark `global_agent_norm_risk: open`, correct the handoff, and do not complete the stage until the risk is resolved or explicitly carried forward.

## Blocking Rules

- Do not skip Stage 2.5 or Stage 4.5.
- Do not change citation style without venue/user justification.
- Do not translate bibliography titles silently.
- Do not mark reviewer concerns addressed without manuscript evidence.
- Do not route to Stage 5 with `source_verification_state.status: fail`.
- Do not collapse `output_language` and `source_language` into one field.
- Do not call shared/global agents from Russian adapters without the audit context above.
