# Russian Academic Pipeline Dashboard

| Stage | Status | Skill | Deliverable | Blocking issues |
|---|---|---|---|---|
| 1 Research | pending/done | akademicheskoe-issledovanie | RQ, literature matrix, verified bibliography |  |
| 2 Writing | pending/done | akademicheskaya-statya | blueprint or draft |  |
| 2.5 Integrity | pending/pass/fail | integrity check | claim/citation/data verification |  |
| 3 Review | pending/done | akademicheskii-retsenzent | decision and roadmap |  |
| 4 Revision | pending/done | akademicheskaya-statya | revised manuscript and response letter |  |
| 3' Re-review | pending/done | akademicheskii-retsenzent | issue closure check |  |
| 4.5 Final integrity | pending/pass/fail | integrity check | final verification |  |
| 5 Finalization | pending/done | akademicheskaya-statya | final package |  |
| 6 Process summary | pending/done | akademicheskii-konveer | process record and AI disclosure summary |  |

## Language And Venue State

- Interaction language:
- Output language:
- Source language:
- Venue/context:
- Citation style:
- Final package mode: RU / EN / bilingual
- Required RU/EN/bilingual components:

## Source Verification State Aggregate

Stable marker: Source verification state.

| Field | Value |
|---|---|
| status | not_started / in_progress / partial / pass / pass_with_notes / fail |
| verified_count |  |
| partial_count |  |
| rejected_count |  |
| unresolved_risks |  |
| last_gate | none / stage_2_5 / stage_4_5 |
| carryover_required | true / false |

## Per-Source Carryover

| source_id | source_language | source_system | verification_status | supports_claims | metadata_missing | unresolved_risks |
|---|---|---|---|---|---|---|
|  | ru/en/other | eLIBRARY/РИНЦ/ВАК/CyberLeninka/DOI/Scopus/WoS/other | verified_current/partially_verified/not_verified/inaccessible/rejected | yes/limited/no |  |  |

## Gate And Checkpoint Carryover

| Carryover item | Status | Blocking? | Evidence needed before clearing |
|---|---|---|---|
| Stage 2.5 integrity gate | pending/pass/pass_with_notes/fail | yes/no |  |
| Stage 4.5 final integrity gate | pending/pass/pass_with_notes/fail | yes/no |  |
| Blocking source issues | open/closed | yes/no |  |
| Open reviewer concerns | open/closed | yes/no |  |
| User checkpoint | required/not_required | yes/no |  |

## Handoff Checklist

| Handoff | Required state carried forward | Present? | Gap |
|---|---|---|---|
| Research -> Writing | RQ, methodology, literature matrix, `source_verification_state`, `output_language`, `source_language`, `final_package_mode` | yes/no |  |
| Writing -> Integrity | draft, claims, bibliography, source additions, checkpoint carryover | yes/no |  |
| Integrity -> Review | Stage 2.5 verdict, unresolved source risks, gate carryover | yes/no |  |
| Review -> Revision | decision, concern IDs, revision roadmap, source-risk carryover | yes/no |  |
| Revision -> Re-review | revised manuscript, response, traceability table, changed claims/sources | yes/no |  |
| Final Integrity -> Finalization | final verification state, package mode, manual checks | yes/no |  |

## Shared/Global Agent Audit

Stable marker: Shared Agent Context Audit.

| Audit item before/after shared agent call | Status | Notes |
|---|---|---|
| Passed Russian venue/context (ВАК/РИНЦ/eLIBRARY/ГОСТ/journal override as applicable) | yes/no/n/a |  |
| Passed separate `output_language` and `source_language` | yes/no/n/a |  |
| Passed `final_package_mode` | yes/no/n/a |  |
| Passed source verification distinctions and unresolved risks | yes/no/n/a |  |
| Checked for English international defaults | yes/no |  |
| `global_agent_norm_risk` | none/open/resolved |  |

## Next Checkpoint

Recommended next stage:

User decision required:

Allowed next stage:

Manual checks before submission:
