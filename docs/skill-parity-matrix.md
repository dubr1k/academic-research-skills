# Skill Parity Matrix

This matrix tracks how the Russian adapter layer maps to the upstream Academic Research Skills package.

Upstream snapshot for the current Russian layer: `175f79bcca4467949fa94e410c25823bd574f687` (`v3.12.0`, 2026-06-08).

## Summary

| Upstream skill | Russian adapter | Current status | Notes |
|---|---|---|---|
| `deep-research` | `akademicheskoe-issledovanie` | Compact adapter | Covers research, literature review, fact-check, systematic review, Russian source context. |
| `academic-paper` | `akademicheskaya-statya` | Compact adapter | Covers planning, drafting, abstract, revision, citation check, formatting, disclosure. |
| `academic-paper-reviewer` | `akademicheskii-retsenzent` | Compact adapter | Covers pre-submission review, methodology review, ВАК/РИНЦ checks, re-review. |
| `academic-pipeline` | `akademicheskii-konveer` | Compact adapter | Covers entry-point detection, staged workflow, integrity gates, review/revision/finalization. |

## Preserved Upstream Core

These directories remain the English/international core and should stay close to upstream:

- `deep-research/`
- `academic-paper/`
- `academic-paper-reviewer/`
- `academic-pipeline/`
- `shared/`
- `agents/`
- `commands/`
- `scripts/`
- `evals/`

## Russian Adapter Scope

The Russian adapters add context-specific behavior rather than translating every upstream file:

- Russian trigger phrases and task descriptions;
- ГОСТ Р 7.0.5-2008 defaults and bibliography reminders;
- ВАК/РИНЦ/eLIBRARY/CyberLeninka context;
- Russian dissertation, ВКР and local journal signals;
- Russian academic style checks;
- Russian AI-cliche checks;
- Opencode `task()` orchestration notes.

## Gap List

| Area | Gap | Priority |
|---|---|---|
| Routing | No executable router; rules live in docs, commands, examples, and tests. | P2 |
| Commands | `/ars-ru-*` slash commands exist for the 4 Russian adapters. | Done |
| Frontmatter | Russian skills share a required metadata schema. | Done |
| References | Each Russian skill has a first local `references/` asset for source verification, ГОСТ, ВАК/РИНЦ review, or bilingual handoffs. | P2 |
| Templates | Each Russian skill has a first local `templates/` asset for literature matrix, ВАК article package, review traceability, or pipeline dashboard. | P2 |
| Evals | Lightweight Russian context fixtures exist; deep quality evals are still pending. | P2 |
| Plugin metadata | One bilingual plugin bundle exposes both English and Russian skills through `skills/`. | Done |
| Upstream sync | Dedicated sync workflow exists in `docs/upstream-sync.md`. | Done |

## Do Not Blindly Port

These upstream areas should be reviewed before Russian adaptation:

- complex agent contracts;
- calibration and claim-audit evals;
- plugin hooks;
- disclosure policies tied to international venues;
- language-specific writing-quality heuristics;
- citation-format logic that assumes APA/Chicago/MLA/IEEE/Vancouver but not ГОСТ.

## Update Checklist

When upstream changes:

1. Fetch upstream.
2. Compare latest upstream against the snapshot hash above.
3. Update the English core without translating it in place.
4. Review changed upstream skill behavior against this matrix.
5. Port only relevant ideas into `russian-academic-skills/`.
6. Update snapshot hash in every Russian `SKILL.md`.
7. Update this matrix.
8. Run bilingual docs/routing tests.
