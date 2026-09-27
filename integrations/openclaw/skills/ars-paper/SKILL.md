---
name: ars-paper
description: "Academic Research Skills: план, черновик, цитирование или ревизия научной статьи в OpenClaw Research."
---

# ARS Paper for OpenClaw

Use the canonical ARS repository identified in the Research workspace's `AGENTS.md`. Source procedures: `academic-paper/SKILL.md` and `russian-academic-skills/akademicheskaya-statya/SKILL.md` (CC BY-NC 4.0; upstream Cheng-I Wu, Russian adaptation dubr1k). This adapter does not activate their Claude Code/OpenCode agents, hooks, or cross-model calls.

1. Select one requested mode: `plan`, `outline-only`, `full`, `abstract-only`, `lit-review`, `revision`, `revision-coach`, `citation-check`, `format-convert`, or `disclosure`. Identify paper type, language, target venue, source materials, length, and output format. Resolve material ambiguity before writing. **Done:** deliverable and evidence boundary are explicit.
2. Read the corresponding source skill's mode section and only necessary references. Russian/GOST work follows the Russian adapter; international-venue instructions take precedence when the target venue specifies its own format. Use `ars-research` when additional source discovery or verification is needed. **Done:** the selected writing procedure has its required inputs.
3. Produce only the requested phase. Keep a claim/source ledger and distinguish supplied findings from proposed wording. Do not invent data, results, DOI, page numbers, references, author contributions, or journal policy. Use OfficeCLI skills and `research-artifact-production` for DOCX; preserve the original manuscript and write an output copy. **Done:** each sourced claim and reference can be audited.
4. For `revision`, compare old and new claim strength, sample limits, qualifiers, null results, and reviewer concerns before accepting edits. Keep a versioned original, revised copy, change log, and response-to-reviewers mapping when requested. Do not claim ARS deterministic patch/guard checks unless the actual repository scripts were run and their reports inspected. **Done:** changed claims have explicit authority and no silent strengthening.
5. Verify citations against inspected sources and render/inspect file output. Report the exact checks run, gaps, and venue-specific requirements still needing human confirmation. **Done:** the requested artifact is complete and its evidence status is stated.

Execute sequentially with OpenClaw tools; do not emit or attempt `task()` or `@agent` commands in this runtime.
