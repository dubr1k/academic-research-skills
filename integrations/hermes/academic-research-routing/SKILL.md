---
name: academic-research-routing
description: "Use when routing RU/EN academic work or screening."
version: 1.1.0
license: CC-BY-NC-4.0
author: Hermes Agent; academic methods by dubr1k/academic-research-skills contributors
metadata:
  hermes:
    tags: [academic-research, routing, bilingual, evidence, integrity]
    related_skills: [deep-research, academic-paper, academic-paper-reviewer, academic-pipeline, akademicheskoe-issledovanie, akademicheskaya-statya, akademicheskii-retsenzent, akademicheskii-konveer, sr-screener]
  source:
    repository: https://github.com/dubr1k/academic-research-skills
    suite_version: 3.23.0
    verified_main_commit: 578daef8e09d33d8561b4acb5ac946a3222cf056
---

# Academic Research Routing — Hermes adapter

## Overview

This is a thin Hermes-native router, not a substitute for the installed academic methods. It chooses one primary route, loads the exact matching skill with `skill_view`, then applies shared evidence and integrity gates. Never emulate a missing skill from memory.

## When to Use

Use for RU/EN research, literature synthesis, manuscript writing, peer review, source verification, an end-to-end research-to-publication pipeline, or explicitly requested screening of existing records. This router selects one installed v3.23.0 method; it does not replace it.

## Required Workflow

1. **Intake.** Identify deliverable, interaction/output language, source languages, materials, stage, venue, citation style, deadline, and whether the work is assessed student work. Ask one focused question only if ambiguity changes the route or integrity boundary.
2. **Choose exactly one primary route.** Use the matrix below. Secondary needs become later stages, not concurrent primary routes.
3. **Check availability.** Use `skills_list` in the active Hermes profile and verify the selected name is installed in that profile's sibling `academic-suite` directory (resolve paths from `skill_view`). Do not use profile `default` or a scratch checkout as a fallback. Stop with an actionable dependency error if missing.
4. **Mandatory load.** Call `skill_view(name="<selected-skill>")` before substantive work. Follow that skill's full method and linked references.
5. **Plan artifacts.** For large work, use staged files in the active project; use tracked background processes or bounded parallel delegation only when size or independent workstreams justify it.
6. **Apply gates.** Source, claim, citation, fabrication, student-work and final-integrity gates below are mandatory.
7. **Deliver.** State selected route/skill, verification limits, unresolved risks and artifact paths. Do not claim checks that were not executed.

## Route Matrix

| Primary route | RU/mixed institutional context | EN/international context |
|---|---|---|
| Research, literature review, systematic review, fact/claim check | `akademicheskoe-issledovanie` | `deep-research` |
| Manuscript plan, drafting, revision, response to reviewers | `akademicheskaya-statya` | `academic-paper` |
| Peer/methodology/readiness review | `akademicheskii-retsenzent` | `academic-paper-reviewer` |
| Full research → paper → review → revision pipeline | `akademicheskii-konveer` | `academic-pipeline` |
| Explicit protocol-driven screening of existing records/full texts, or reporting an already completed screening run | `sr-screener` | `sr-screener` |

Screening is opt-in: require an explicit existing-records/protocol screening request, protocol setup for that screening task, or a request to report a completed screening run. A generic systematic review, literature review, PRISMA request or research handoff never automatically selects `sr-screener`. Keep these on the research route unless the user explicitly requests screening; missing records/protocol are an intake gate, not permission to invent them.

Prefer RU/mixed when ГОСТ, ВАК, РИНЦ, eLIBRARY, CyberLeninka, Russian dissertation/VKR or mixed RU/EN sources dominate. Prefer EN/international for Scopus/WoS, APA/IEEE/Vancouver, English manuscripts and international review. Output language follows the user, not merely the selected route.

## Evidence and Integrity Gates

- **Source gate:** each substantial factual/bibliographic claim has a source, user-provided material, or explicit `hypothesis/interpretation/unverified` label.
- **Verification gate:** distinguish `verified_current`, `partially_verified`, `not_verified`, `inaccessible`, and `rejected`.
- **Claim gate:** a distorted, inaccessible or unverifiable source cannot support a proved claim.
- **Citation gate:** every in-text citation resolves to a bibliography entry; every bibliography entry is used or explicitly marked further reading.
- **Fabrication gate:** never invent DOI, authorship, page range, issue, quotation, method, sample, finding or review comment.
- **Integrity gate:** before final scholarly delivery, check source/claim traceability, citation bijection, scope, limitations and unsupported certainty.
- **Student-work gate:** provide critique, questions, scaffolds, rubrics, structure and revision guidance. Do not silently produce submission-ready assessed work as if authored by the student. Explicit drafting requests still require transparency and institutional constraints.

## Hermes Runtime Mapping

- Skills: `skills_list` → `skill_view`; never rely on `.claude`, OpenClaw topics or foreign slash commands.
- Files: `read_file`, `search_files`, `write_file`, `patch`; put large artifacts in the user-approved project.
- Literature/current facts: `arxiv` and web tools when available; search snippets are discovery aids, not evidence.
- Documents: `ocr-and-documents` and native document extraction.
- Long work: visible `terminal(background=true, notify=true)` for durable bounded work; otherwise bounded `delegate_task` for independent reasoning workstreams.
- Foreign `Workflow`/`Agent`/Task invocations are methodology roles, not installed Hermes tools. Map them to separate-context `delegate_task` workers when available. This is conversational isolation, not OS/process/filesystem/tool isolation; shared tools can read shared files. Never claim blinded or machine-enforced isolation without actual access controls and receipts. If delegation is unavailable, disclose the missing independent reviewer and pause at mandatory independence gates.
- The main assistant writes substantive research/manuscript text itself, per the user's preference. Delegate bounded search, extraction, checking, critique and evidence tables, not final prose authorship. Carry the upstream role prompts, typed contracts, pilot/QC, human decisions and evidence gates into each worker; do not convert them into a one-pass imitation.
- Model names/tiers in upstream screening templates are foreign defaults, not authorization to change Hermes providers/models. Resolve available capabilities explicitly, disclose substitutions and do not claim cross-model checks without executing them.
- Resolve `SUITE_ROOT` as the installed sibling `academic-suite` directory (from the path returned by `skill_view`), never the manuscript CWD or a scratch checkout. Run bundled `scripts/` and `sr-screener/scripts/` from that root with explicit absolute artifact paths. Keep `shared/`, `tests/`, fixtures and all support roots together. No hook/plugin/Workflow auto-installation is implied.
- For local business-material research, also load `references/applied-business-materials-audit.md`; do not treat commercial market signals as proved market-size claims.
- Read `references/hermes-runtime-contract.md` before runtime execution, screening delegation, ledger recovery or RU/EN abstract generation.
- Delivery: use the current surface's supported artifact delivery; in a plain CLI return the artifact path. Do not hardcode channel targets or promise messaging delivery.
- Environment: do not mutate Hermes config, provider, model, memory, cron or Obsidian.

## Completion Checklist

- [ ] Exactly one primary route selected and named
- [ ] Matching installed skill loaded via `skill_view`
- [ ] User materials and output language recorded
- [ ] Student-work boundary resolved
- [ ] Evidence/claim verification states visible
- [ ] Citation and fabrication gates passed
- [ ] Limitations and unresolved risks disclosed
- [ ] Final artifact verified and actually delivered
