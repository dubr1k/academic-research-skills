---
name: ars-pipeline
description: "Academic Research Skills: связать исследование, статью, проверку, рецензию и ревизию в OpenClaw Research."
---

# ARS Pipeline for OpenClaw

Use the canonical ARS repository identified in the Research workspace's `AGENTS.md`. Source procedures: `academic-pipeline/SKILL.md` and `russian-academic-skills/akademicheskii-konveer/SKILL.md` (CC BY-NC 4.0; upstream Cheng-I Wu, Russian adaptation dubr1k). This is an OpenClaw phase-by-phase adapter, not a claim that the upstream 10-stage Claude/OpenCode runtime is installed.

1. Inventory available materials: topic/RQ, source corpus, draft, review, response letter, revised manuscript, venue rules. Determine entry stage and requested exit stage. For a request covering only one stage, use `ars-research`, `ars-paper`, or `ars-review` directly. **Done:** stage scope and expected artifacts are named.
2. Read the applicable source pipeline skill and its relevant handoff/integrity references. Record interaction, source, and output languages separately. Define allowed output files for each phase before work begins. **Done:** stage inputs, outputs, and write boundaries are explicit.
3. Run requested stages sequentially: research → write → claim/citation/data integrity → review → revision → re-review → final integrity → finalization. At each boundary, keep source verification state, artifact paths and versions, unresolved issues, and the next-stage decision. Do not advance through a failed or incomplete integrity gate as if it passed. **Done:** every completed stage has inspectable output and a handoff record.
4. Use `ars-research`, `ars-paper`, and `ars-review` for their respective work. Research currently has no delegation; do not issue OpenCode `task()`/Claude `@agent`, claim independent panels, or imply that optional hooks, cross-model checks, and deterministic ARS scripts ran. Execute a source-repo script only when its prerequisites, inputs, effects, and output checks have been inspected for this task. **Done:** runtime claims match actions actually taken.
5. Deliver the finished requested package or a truthful checkpoint: completed stages, artifact paths, passed/failed/not-run gates, remaining evidence gaps, and the next stage. **Done:** status is reproducible without relying on unverified pipeline claims.
