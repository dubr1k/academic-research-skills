---
name: ars-review
description: "Academic Research Skills: рецензирование статьи, методологии или повторная проверка правок в OpenClaw Research."
---

# ARS Review for OpenClaw

Use the canonical ARS repository identified in the Research workspace's `AGENTS.md`. Source procedures: `academic-paper-reviewer/SKILL.md` and `russian-academic-skills/akademicheskii-retsenzent/SKILL.md` (CC BY-NC 4.0; upstream Cheng-I Wu, Russian adaptation dubr1k).

1. Identify the manuscript version, target venue, discipline, review mode (`quick`, `full`, `methodology`, or `re-review`), and supplied data/sources. Preserve the submitted file; write reports separately. **Done:** review scope and manuscript identity are explicit.
2. Read the selected source skill and the references required for that mode. Inspect the actual manuscript, figures, tables, methods, citations, and relevant venue rules. Record pages/sections for each finding. **Done:** findings refer to inspected text, not filenames or abstracts.
3. Review distinct dimensions: venue fit and contribution, methodology and causal strength, domain/literature coverage, alternative interpretations, and adversarial weaknesses. Keep the observations separate before synthesis. This Research agent works alone: label the result a **single-agent multi-perspective review**, never an independent five-reviewer panel or blinded evaluation. **Done:** each major criticism has a locator, rationale, and actionable remedy.
4. For re-review, compare the original manuscript, reviewer comments, revision, and response letter. Separate implemented changes from asserted changes; flag new claim drift or missing evidence. Do not state that ARS hash-bound or deterministic re-review gates ran unless their scripts were actually executed and reports verified. **Done:** every tracked concern has a disposition.
5. Return a concise review with strengths, major/minor issues, evidence uncertainty, prioritized revision roadmap, and the exact verification performed. Editorial decisions are advisory, not a real journal decision. **Done:** the requester can act on every material issue.

Do not call OpenCode `task()`, Claude `@agent`, or unsupported hooks. A genuinely independent panel requires separate configured reviewers and a separately verified workflow.
