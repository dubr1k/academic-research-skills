# Context Adaptation Audit

This audit records which repository surfaces already understand multiple academic contexts and which surfaces still need adaptation. It is intentionally separate from `docs/bilingual-routing.md`: routing says which skill to choose; this document says where the repo still needs context-aware assets, tests, or maintenance rules.

## Context Axes

Every bilingual change should be checked against these axes:

- Request language: English, Russian, or mixed RU/EN.
- Target venue: English international, Russian journal, ВАК journal, РИНЦ/eLIBRARY-indexed venue, dissertation council, or mixed/international workflow with Russian sources.
- Citation style: ГОСТ, APA, IEEE, Vancouver, Chicago, MLA, or journal-specific override.
- Corpus shape: English sources, Russian sources, mixed corpus, CyberLeninka access copy, eLIBRARY metadata, DOI-first source, or user-provided incomplete metadata.
- Output language: answer in the user's language by default, but preserve explicit output language requests for abstracts, reviewer replies, and final manuscript sections.
- Source metadata: preserve `source_language`, original titles, access channel, verification status, and missing-field markers.
- Integrity gates: source verification, claim support, citation verification, reviewer response traceability, and no invented bibliographic metadata.

## Current Coverage

| Surface | Current state | Context adaptation status |
| --- | --- | --- |
| `README.md` | Bilingual landing page with EN/RU entry points. | Good first-entry coverage; points to routing and Russian context docs. |
| `README.ru.md` | Detailed Russian usage guide. | Covers ГОСТ, ВАК, РИНЦ, eLIBRARY, CyberLeninka, and mixed citation styles. |
| `README.en.md` | Preserved upstream English guide. | Keep close to upstream; do not translate in place unless upstream itself changes. |
| `docs/bilingual-routing.md` | Defines EN/RU/mixed skill selection. | Core routing layer for English international, Russian journal, and mixed RU/EN workflows. |
| `docs/russian-academic-context.md` | Russian academic conventions and local-source integrity rules. | Covers ГОСТ Р 7.0.5-2008, ВАК/РИНЦ separation, source verification, style cliches, and traceability. |
| `docs/skill-parity-matrix.md` | Maps upstream skills to Russian adapters. | Useful for upstream sync; should be revisited after each Russian asset expansion. |
| `docs/upstream-sync.md` | Explains origin/upstream sync and snapshot updates. | Covers maintenance context; should explicitly trigger this audit after future upstream releases. |
| `commands/` | Upstream `/ars-*`, four `/ars-ru-*` commands, and `/ars-auto`. | Explicit and automatic routing entrypoints exist; `/ars-auto` surfaces selected skill, language, venue, citation style, source policy, and warnings. |
| `skills/` | Bilingual plugin-facing bundle with EN and RU skills. | Packaged, but should be checked whenever Russian adapters gain new local assets. |
| `russian-academic-skills/` | Four Russian adapter skills with local `agents/`, `references/`, and `templates`; research, writing, reviewer, and pipeline adapters now have first depth-pass coverage. | Functional adapter layer; future work can add richer examples, LLM-judged evals, and upstream-sync maintenance. |
| `agents/` | Shared upstream English/global agents. | Not yet context-aware; global shared agents can silently assume English/international norms. |
| `academic-paper/agents/` | English paper-writing agents, including bilingual abstract support. | Strong upstream coverage; Russian context should stay in adapters unless a shared bilingual handoff is required. |
| `deep-research/agents/` | English research agents with source verification. | Good international-source layer; Russian source verification remains adapter-specific. |
| `examples/ru/` | Russian examples for research, paper, reviewer, re-review, pipeline, ВАК package, РИНЦ/eLIBRARY status, and dissertation council review. | Good venue-specific coverage for Russian academic workflows. |
| `examples/bilingual/` | Mixed Scopus/APA, CyberLeninka/Scopus, APA override, source handoff, bilingual pipeline, Scopus/WoS Russian-source, and journal override final-package workflows. | Good mixed RU/EN coverage with venue-specific final packages. |
| `evals/gold/russian_academic_quality/` | Russian advisory-calibration gold set. | Measured by `scripts/run_evals.py`; covers ГОСТ bibliography, ВАК/РИНЦ review, source verification, style, traceability, mixed routing. |
| `evals/gold/russian_academic_quality_judged/` | Russian recorded-output judged gold set. | First LLM-output judged layer over cached `model_output` text; live LLM judging remains future advisory work. |
| `scripts/run_evals.py` | Native measurers for `russian_academic_quality` and `russian_academic_quality_judged`. | Structural and recorded-output Russian evals now both run through the harness. |
| `.claude-plugin/plugin.json` | Bilingual plugin metadata for Claude Code. | Good high-level bilingual package signal. |
| `.codex-plugin/plugin.json` | Codex-compatible bilingual metadata. | Good high-level bilingual package signal. |

## Adaptation Gaps

### P3a: Audit Baseline

This document is the baseline context-adaptation inventory. Future P3 work should update it whenever a surface moves from "gap" to "covered".

Primary surfaces: `docs/context-adaptation-audit.md`, `PLAN.md`, `tests/test_context_adaptation_audit.py`.

### P3b: Russian Source Verification Depth

Status: covered in the first depth pass.

The research adapter now has deeper examples and checklists for:

- eLIBRARY metadata that does not prove РИНЦ or ВАК status;
- CyberLeninka as an access channel, not peer-review proof;
- DOI values that are shape-valid but unverified;
- incomplete Russian bibliographic records that require `metadata_missing`;
- mixed corpus tracking where `source_language` must survive synthesis;
- `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, and rejected-source status handling.

Primary surfaces: `russian-academic-skills/akademicheskoe-issledovanie/`, `examples/ru/research-source-verification-depth.md`, `examples/bilingual/mixed-source-verification-handoff.md`, `evals/gold/russian_academic_quality/`.

### P3c: ГОСТ Bibliography and Journal Override Depth

Status: covered in the first depth pass.

The writing adapter now has deeper assets for:

- ГОСТ bibliography variants by source type: journal article, monograph, dissertation abstract, conference paper, web source;
- conflict rules where a Russian journal asks for APA, IEEE, Vancouver, or Chicago instead of ГОСТ;
- bilingual abstract handoff: Russian manuscript with English abstract, English manuscript for Russian venue;
- explicit no-guessing rules for pages, issue number, publisher, city, and DOI.

Primary surfaces: `russian-academic-skills/akademicheskaya-statya/`, `examples/ru/paper-gost-source-types.md`, `examples/bilingual/russian-journal-apa-override.md`, `evals/gold/russian_academic_quality/`.

### P3d: ВАК/РИНЦ Review and Re-review Traceability

Status: covered in the first depth pass.

The reviewer adapter now has deeper assets for:

- separating journal-index status from manuscript quality;
- review criteria for ВАК article, dissertation council, and international journal review;
- re-review status taxonomy: addressed, partially addressed, not addressed, needs evidence;
- page/section-level traceability before marking reviewer comments resolved.

Primary surfaces: `russian-academic-skills/akademicheskii-retsenzent/`, `examples/ru/reviewer-rereview-traceability.md`, `evals/gold/russian_academic_quality/`.

Stable markers: `journal-index status`, `manuscript quality`, `needs_evidence`.

### P3e: Bilingual Pipeline Handoff and Global Shared Agents

Status: covered in the first depth pass.

The pipeline adapter now has deeper assets for:

- bilingual pipeline handoff between research, writing, review, and revision;
- source verification state carried across stages;
- output language and source language tracked separately;
- final package modes: RU, EN, or bilingual;
- `agents/` global shared agents that should not assume English international norms when called from Russian adapters.

Primary surfaces: `russian-academic-skills/akademicheskii-konveer/`, `examples/bilingual/pipeline-bilingual-handoff.md`, `examples/ru/pipeline-dissertation-to-article.md`.

Stable markers: `source verification state`, `output_language`, `source_language`, `final_package_mode`, `global_agent_norm_risk`.

### P3f: Auto/router Entrypoint

Status: covered in the first depth pass.
Stable marker: auto/router entrypoint.

Explicit `/ars-ru-*` commands exist, upstream `/ars-*` commands remain intact, and `/ars-auto` now lets users provide a task without choosing EN/RU manually. It applies `docs/bilingual-routing.md` and surfaces the chosen context:

- `selected_skill`;
- `request_language`;
- `output_language`;
- `venue`;
- `citation_style`;
- `source_language` policy;
- warnings for ГОСТ vs APA/IEEE/Vancouver/Chicago conflicts.

Primary surfaces: `commands/ars-auto.md`, `docs/bilingual-routing.md`, `tests/fixtures/bilingual_routing_cases.json`.

### Post-P3b: Venue-specific Examples

Status: covered in the first venue-specific pass.

The examples layer now has dedicated venue fixtures for:

- ВАК submission package with ГОСТ default and journal override decision;
- РИНЦ/eLIBRARY current status evidence and journal-index status separation;
- dissertation council review, автореферат, traceability, and page/section evidence;
- Scopus/WoS English article planning with Russian sources and preserved `source_language`;
- bilingual final package with APA journal override and `final_package_mode`.

Primary surfaces: `examples/ru/venue-vak-submission-package.md`, `examples/ru/venue-rinc-elibrary-status-check.md`, `examples/ru/venue-dissertation-council-review.md`, `examples/bilingual/venue-scopus-wos-russian-sources.md`, `examples/bilingual/venue-journal-override-final-package.md`.

### Post-P3c: Upstream Sync v3.12.1

Status: covered for upstream snapshot `88fc003e6abf5fe9fe86dc8200f8d4aa8d511956` (`v3.12.1`, 2026-06-17).

The English core has been merged from `upstream/main`. The bilingual fork keeps `README.md`, plugin metadata, Russian adapters, and bilingual docs as overlay surfaces, while `README.en.md` tracks the upstream English README.

### Post-P3d: Candidate Output Capture

Status: covered for the first recorded-output capture pass.

The judged Russian eval now mirrors every `model_output` fixture into `candidate_outputs/baseline/*.md` with a SHA-256 `manifest.json`. `scripts.capture_russian_academic_quality_outputs` can regenerate the capture or run `--check` to detect drift before future live/cached judges consume the files.

Primary surfaces: `evals/gold/russian_academic_quality_judged/candidate_outputs/baseline/`, `scripts/capture_russian_academic_quality_outputs.py`, `scripts/test_capture_russian_academic_quality_outputs.py`.

## Recommended Order

1. Add cached judge verdict fixtures and dimension-level metrics on top of captured candidate outputs.
2. Run the upstream sync workflow again after the next upstream release and update this audit.

The core P3 adapter-depth pass is covered. Future work should preserve the same pattern: add concrete assets first, then examples, then eval/test coverage, then update this audit.
