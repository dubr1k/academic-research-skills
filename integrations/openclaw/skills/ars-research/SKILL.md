---
name: ars-research
description: "Academic Research Skills: исследование, обзор литературы, fact-check или systematic review в OpenClaw Research."
---

# ARS Research for OpenClaw

Use the canonical ARS repository identified in the Research workspace's `AGENTS.md`. This adapter is based on the repository's `deep-research/` and `russian-academic-skills/akademicheskoe-issledovanie/` skills (CC BY-NC 4.0; upstream Cheng-I Wu, Russian adaptation dubr1k). It preserves their research method, not their Claude Code or OpenCode execution machinery.

1. Classify the request as `socratic`, `quick`, `fact-check`, `lit-review`, `full`, or `systematic-review`. Record the research question, corpus, date range, output, and stop condition. If the question is too vague to choose a mode, ask one focused question. **Done:** scope and mode are explicit.
2. Read the relevant original `SKILL.md` and only the branch-specific references needed for the task. For Russian sources, read `russian-academic-skills/akademicheskoe-issledovanie/references/russian-source-verification.md`; for Russian legal claims also read `russian-legal-regulatory-research.md`. The requested publication venue's current requirements override generic ARS formatting. **Done:** the source procedure and applicable branch are identified.
3. Execute the procedure with OpenClaw's allowed tools: Firecrawl search/scrape, direct OpenAlex/Crossref queries, local file/PDF tools, and OfficeCLI when an artifact is requested. Replace ARS `@agent` and OpenCode `task()` calls with bounded sequential work. Research currently forbids delegation; never claim a 13-agent run or independent cross-model verification. **Done:** every load-bearing source has been opened, not merely found in search results.
4. Maintain a claim → inspected source → exact locator → verification status ledger. Deduplicate literature by DOI or stable identifier, check bibliographic metadata separately from substantive findings, preserve original title/citation language, and mark inaccessible or contradictory evidence. For systematic reviews, state databases, query strings, inclusion/exclusion decisions, retrieval date, and an honest flow count; do not claim PRISMA, risk-of-bias, GRADE, or meta-analysis steps that were not actually executed. **Done:** all substantive claims have support or a visible limitation.
5. Return the requested brief or artifact with method, source links, search log where material, limitations, and the exact verification performed. Use `research-control` for citation discipline and `research-artifact-production` for files. **Done:** output is readable, evidence-backed, and scoped to the request.

Do not run ARS installation scripts, hooks, cache invalidation, cross-model API calls, or `--dangerously-skip-permissions` merely because the source repository documents them. Optional machinery requires a separate supported implementation and verification.
