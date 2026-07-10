# Skill Parity Matrix

This matrix tracks how the Russian adapter layer maps to the upstream Academic Research Skills package.

Upstream snapshot for the current Russian layer: `ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c` (`v3.15.0`, 2026-07-08).

## Summary

| Upstream skill | Russian adapter | Current status | v3.15 adaptation |
|---|---|---|---|
| `deep-research` | `akademicheskoe-issledovanie` | Active compact adapter | Adjacent-framing probe adapted for Russian institutional/regional frames; OpenAlex API-key, budget-aware 429 and arXiv backoff semantics preserve fail-closed source status. |
| `academic-paper` | `akademicheskaya-statya` | Active compact adapter | Write-scope/phase-boundary rules mapped to Claude hooks and explicit Opencode/Codex task allowlists; optional guard never replaces citation/claim audit. |
| `academic-paper-reviewer` | `akademicheskii-retsenzent` | Active compact adapter | READ-ONLY contract remains effective when optional hook degrades; ambiguous review/revision inputs require clarification. |
| `academic-pipeline` | `akademicheskii-konveer` | Active compact adapter | Runtime guard state is carried explicitly while mandatory Stage 2.5/4.5 and RU/EN handoff gates remain runtime-independent. |

## Preserved Upstream Core

These directories remain the English/international core and should stay close to upstream:

- `deep-research/`, `academic-paper/`, `academic-paper-reviewer/`, `academic-pipeline/`;
- `shared/`, `agents/`, `commands/`, `scripts/`, `evals/`;
- release discipline, command invariants, hook portability and source-client tests.

The fork does not translate these files in place. `README.en.md` mirrors the tracked upstream README; the root README is the bilingual landing page.

## Russian Adapter Scope

The Russian adapters add context-specific behavior rather than translating every upstream file:

- Russian trigger phrases and task descriptions;
- ГОСТ Р 7.0.5-2008 defaults and journal-style overrides;
- ВАК/РИНЦ/eLIBRARY/CyberLeninka context;
- Russian dissertation, ВКР and local journal signals;
- Russian academic style and AI-cliche checks;
- Opencode/Codex orchestration notes and runtime-neutral phase boundaries;
- bilingual source/language/venue state and integrity-gate carryover.

## v3.13-v3.15 Capability Review

| Upstream change | English core | Russian adapter action | Parity |
|---|---|---|---|
| Socratic adjacent-framing probe | Preserved verbatim upstream | Adapted in research skill with Russian federal/regional, normative/practice and venue-quality distinctions | Adapted |
| Deterministic PreToolUse write-scope guard | Preserved, including Windows graceful degradation | Writing, reviewer and pipeline skills define equivalent task allowlists and post-task checks outside hook-enabled Claude | Adapted |
| OpenAlex API-key + budget-aware 429; arXiv ToU backoff | Preserved in clients/protocols | Research skill maps budget exhaustion to partial/inaccessible verification, never false verified status | Adapted |
| Explicit marketplace skill paths | Preserved and extended | Manifest explicitly lists all four English and all four Russian skills | Extended |
| SETUP/command/release invariant gates | Preserved | Bilingual metadata/version tests and sync checklist run alongside upstream validators | Extended |
| `THIRD_PARTY.md` and Korean README | Preserved | Root bilingual README links both without changing attribution/endorsement semantics | Documented |

## Gap List

| Area | Gap | Priority |
|---|---|---|
| Routing | No executable bilingual router; rules live in docs, commands, examples, and tests. | P2 |
| Commands/frontmatter/plugin metadata | Four `/ars-ru-*` commands, common metadata schema and one explicit 8-skill bundle exist. | Done |
| References/templates/agents | Every Russian skill has local context assets; deeper v3.15 feature-specific agent fixtures can still be expanded. | P2 |
| Evals | Russian fixture and judged-quality suites exist; live API behavior remains covered primarily by upstream client tests. | P2 |
| Runtime parity | Opencode/Codex cannot use Claude PreToolUse hooks; explicit task scopes and post-task diff checks are the documented fallback. | Accepted |
| Upstream sync | Dedicated workflow and snapshot assertions exist. | Done |

## Do Not Blindly Port

Review before adaptation: complex agent contracts, calibration and claim-audit evals, plugin hooks, international disclosure policies, language-specific style heuristics, and citation logic that omits ГОСТ. Optional runtime hardening must not be presented as a universal integrity guarantee.

## Update Checklist

1. Fetch upstream and compare against the snapshot above.
2. Merge English core without translating it in place.
3. Review changed behavior across all four skill families.
4. Adapt relevant ideas under `russian-academic-skills/`.
5. Update all four snapshot/version/date blocks, README surfaces and plugin manifests.
6. Update this matrix and feature-specific assertions.
7. Run bilingual tests, all upstream validators and the full pytest suite.
