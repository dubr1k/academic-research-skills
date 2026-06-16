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
| `commands/` | Upstream `/ars-*` plus four `/ars-ru-*` commands. | Explicit Russian commands exist; missing an auto/router entrypoint that exposes context selection without forcing users to choose. |
| `skills/` | Bilingual plugin-facing bundle with EN and RU skills. | Packaged, but should be checked whenever Russian adapters gain new local assets. |
| `russian-academic-skills/` | Four Russian adapter skills with first local `agents/`, `references/`, and `templates/`. | Functional adapter layer; not yet as deep as upstream English skill folders. |
| `agents/` | Shared upstream English/global agents. | Not yet context-aware; global shared agents can silently assume English/international norms. |
| `academic-paper/agents/` | English paper-writing agents, including bilingual abstract support. | Strong upstream coverage; Russian context should stay in adapters unless a shared bilingual handoff is required. |
| `deep-research/agents/` | English research agents with source verification. | Good international-source layer; Russian source verification remains adapter-specific. |
| `examples/ru/` | Russian examples for research, paper, reviewer, and pipeline. | Good basic coverage; needs more edge cases for incomplete metadata and journal-specific overrides. |
| `examples/bilingual/` | Mixed Scopus/APA and CyberLeninka/Scopus workflows. | Good mixed RU/EN coverage; should add reviewer-response and bilingual abstract examples. |
| `evals/gold/russian_academic_quality/` | Russian advisory-calibration gold set. | Measured by `scripts/run_evals.py`; covers ГОСТ bibliography, ВАК/РИНЦ review, source verification, style, traceability, mixed routing. |
| `scripts/run_evals.py` | Native measurer for `russian_academic_quality`. | Good structural measurement; future work can add LLM-output judged evals separately. |
| `.claude-plugin/plugin.json` | Bilingual plugin metadata for Claude Code. | Good high-level bilingual package signal. |
| `.codex-plugin/plugin.json` | Codex-compatible bilingual metadata. | Good high-level bilingual package signal. |

## Adaptation Gaps

### P3a: Audit Baseline

This document is the baseline context-adaptation inventory. Future P3 work should update it whenever a surface moves from "gap" to "covered".

Primary surfaces: `docs/context-adaptation-audit.md`, `PLAN.md`, `tests/test_context_adaptation_audit.py`.

### P3b: Russian Source Verification Depth

The research adapter has a first source-verification agent and reference, but Russian source handling still needs deeper examples and checklists for:

- eLIBRARY metadata that does not prove РИНЦ or ВАК status;
- CyberLeninka as an access channel, not peer-review proof;
- DOI values that are shape-valid but unverified;
- incomplete Russian bibliographic records that require `metadata_missing`;
- mixed corpus tracking where `source_language` must survive synthesis.

Primary surfaces: `russian-academic-skills/akademicheskoe-issledovanie/`, `examples/ru/`, `examples/bilingual/`, `evals/gold/russian_academic_quality/`.

### P3c: ГОСТ Bibliography and Journal Override Depth

The writing adapter has a first ГОСТ bibliography guide and ВАК package template. It still needs deeper assets for:

- ГОСТ bibliography variants by source type: journal article, monograph, dissertation abstract, conference paper, web source;
- conflict rules where a Russian journal asks for APA, IEEE, Vancouver, or Chicago instead of ГОСТ;
- bilingual abstract handoff: Russian manuscript with English abstract, English manuscript for Russian venue;
- explicit no-guessing rules for pages, issue number, publisher, city, and DOI.

Primary surfaces: `russian-academic-skills/akademicheskaya-statya/`, `academic-paper/templates/`, `examples/ru/paper-abstract-gost.md`, `commands/ars-ru-paper.md`.

### P3d: ВАК/РИНЦ Review and Re-review Traceability

The reviewer adapter has a first ВАК/РИНЦ criteria reference and traceability template. It still needs deeper assets for:

- separating journal-index status from manuscript quality;
- review criteria for ВАК article, dissertation council, and international journal review;
- re-review status taxonomy: addressed, partially addressed, not addressed, needs evidence;
- page/section-level traceability before marking reviewer comments resolved.

Primary surfaces: `russian-academic-skills/akademicheskii-retsenzent/`, `examples/ru/reviewer-vak-rinc.md`, `evals/gold/russian_academic_quality/`.

### P3e: Bilingual Pipeline Handoff and Global Shared Agents

The pipeline adapter has first handoff contracts, but shared orchestration surfaces still skew upstream-English. The next deeper layer should cover:

- bilingual pipeline handoff between research, writing, review, and revision;
- source verification state carried across stages;
- output language and source language tracked separately;
- final package modes: RU, EN, or bilingual;
- `agents/` global shared agents that should not assume English international norms when called from Russian adapters.

Primary surfaces: `russian-academic-skills/akademicheskii-konveer/`, `agents/`, `academic-pipeline/agents/`, `examples/ru/pipeline-dissertation-to-article.md`.

### P3f: Auto/router Entrypoint

Explicit `/ars-ru-*` commands exist, and upstream `/ars-*` commands remain intact. Missing piece: an auto/router entrypoint that lets users provide a task without choosing EN/RU manually. It should apply `docs/bilingual-routing.md` and surface the chosen context:

- selected skill;
- request language;
- output language;
- venue;
- citation style;
- source_language policy;
- warnings for ГОСТ vs APA/IEEE/Vancouver/Chicago conflicts.

Primary surfaces: `commands/`, `docs/bilingual-routing.md`, `tests/fixtures/bilingual_routing_cases.json`.

## Recommended Order

1. P3b: deepen Russian source verification assets and examples.
2. P3c: deepen ГОСТ bibliography and journal override writing assets.
3. P3d: deepen ВАК/РИНЦ review and re-review traceability assets.
4. P3e: adapt bilingual pipeline handoff and inspect global shared agents.
5. P3f: add an auto/router entrypoint only after the four domain adapters have enough depth to route into.

This order keeps the adapter layer useful before adding more routing surface. A router that points to shallow downstream assets would create confidence without enough behavior behind it.
