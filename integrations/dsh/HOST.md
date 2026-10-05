## DSH execution contract (applies to every loaded reference)

This is a DSH-only adapter, not the original Claude Code/OpenCode runtime.
System/developer/user permissions still win. Domain requirements (evidence,
contracts, human checkpoints, integrity gates) remain mandatory. Host dispatch,
model selectors and hook setup in the original documents are **reference only**.
Do not run their foreign API examples or import their host configuration.

### Route first; preflight before work

- A simple factual question uses fact-check/quick with one executor, not an agent
  team or the publication pipeline. Ask about ambiguous intent. Use only the
  requested stage; full pipeline requires an explicit full-cycle request.
- Read the selected source SKILL mode and its referenced domain protocols from
  the pinned source root below. Do not recursively load the whole repository.
- Run the installed `preflight.py` with this overlay's absolute `--skill-dir` and
  selected `--mode`. The command checks pinned resources and baseline mode
  dependencies, **not** scientific gate success. It does not install anything.
- Then read each selected gate script and check its imports, executable/API
  requirements, input schema, credentials availability (never print secrets),
  artifacts and invocation for this actual mode. Check optional extensions
  (systematic review/meta-analysis, PDF extraction, export, online verification,
  cross-model transport) separately. The baseline preflight is not exhaustive.
- Missing dependency/tool/access: record `blocked` or `not_run`, list exact
  missing resources and ask for an approved remedy or narrower scope. Never
  change a mandatory gate to optional, call it passed, fabricate a receipt or
  silently finalize. Stage 2.5 and 4.5 integrity checks remain required.

### Native dispatch translation (no implicit model selection)

| Foreign source notation (reference only) | DSH action |
|---|---|
| `task(category="ultrabrain"/"deep"/"writing")` | A role description in `subagent`'s prompt, or execute directly. No category argument. |
| `task(subagent_type="librarian")` | Available `web_search`/`web_fetch` or a scoped literature-search `subagent`; verify retrieved sources. |
| `task(subagent_type="oracle")`, `Task`, `Agent` | A scoped native `subagent`, not an installed oracle persona. |
| Inherited-context collaborator | `subagent_fork`, only when context inheritance is appropriate. |
| Resume/message child | `send_message` with the returned direct child's `agent_id`. |
| `model:`, `tools:`, `allowed-tools:`, provider/category YAML | Advisory upstream metadata, **not runtime enforcement**; do not pass unsupported keys. |
| `TaskOutput`, team broadcasts, sessions, host hooks | Do not call them. Use native completion notifications and `send_message`; otherwise disclose unsupported behavior. |

Current native calls have no per-agent model/provider selector. Do not claim
Opus/Sonnet/Haiku routing, a different model, or cross-model verification merely
by writing a model name in a prompt. Dedicated external transports are not
configured by this adapter; if a selected protocol requires one, block that
step until it is separately configured and tested. No host hook installation.
Set `write_scope_guard: unsupported`; allowlists and read-only roles are
**prompt-only**, not filesystem sandboxes. Check actual diffs after child work.

Example call shapes (supply the real task and absolute resource paths):

```text
subagent({description: "Verify cited sources", prompt: "Read-only role; do not edit files or start children. Verify the supplied claims against sources, report evidence and limitations. [bounded inputs and output contract]", run_in_background: true})
subagent_fork({description: "Continue shared analysis", prompt: "[scope, ownership, deliverable; not a blind reviewer]", run_in_background: true})
send_message({agent_id: "[returned direct child id]", message: "[bounded follow-up]"})
```

For independent review use a **fresh NONfork `subagent`** and preserve the
source's two-call contract, never collapse precommitment into manuscript review:
- Phase 1 is **paper-content-blind**: supply only authorized field/role metadata
  and contract/rubric material. NO manuscript, abstract, results, author dialogue,
  previous verdicts or other reviewers' reports. Validate/freeze the required
  precommitment before Phase 2; a failed contract blocks progression.
- Phase 2 is paper-visible: supply the manuscript, frozen Phase 1 contract and
  authorized evidence. Use a fresh NONfork subagent with that bounded packet;
  never a fork inheriting author conversation. Exclude other reviewers' reports
  and gold answers; only downstream synthesis may combine independent reports.
For protocols without precommitment use the applicable bounded fresh reviewer
packet. Do not resume a contaminated reviewer. Fresh conversation is not
filesystem isolation or proof of statistical independence; report the shared
runtime/model and prompt-only access boundary. If stronger isolation is required
but unavailable, record it as unsupported, not satisfied.

Start independent delegations together; continue useful parent work. Use native
completion notifications, inspect returned artifacts, and reconcile conflicts.
Do not create children merely to simulate the advertised agent count. The DSH
`workflow` tool is permitted **only when the user explicitly asks for a workflow
or large multi-agent orchestration**, never just because a source calls its
ordinary process a workflow. A full cycle can use ordinary native calls.

### Domain references and path translation

Resolve `scripts/`, `shared/`, and named skill prefixes against the pinned
repository root, not the overlay directory or the user's project. Resolve local
`agents/`, `references/`, `templates/`, `examples/` against the selected source
skill directory. For an ambiguous relative path, inspect both locations; do not
invent files or silently substitute an unrelated script. Use absolute script
and input/output paths; set working directory explicitly when a script requires
it. Keep user artifacts outside the pinned source. Quote paths with spaces.

Templates and source agent cards are domain references only: retain their
schemas, role duties, safety/ethics requirements and evidence criteria; translate
all orchestration through this table before execution. Never blindly copy a
foreign task block into a runnable DSH instruction. If a host-specific action has
no mapping here or no available tool, report unsupported and stop the affected
step. This policy applies transitively to nested references, not just SKILL.md.
Do not execute shell examples without reading the scripts and validating paths.

Preserve source verification state, profile/hash bindings, bilingual handoffs,
reviewer findings, revision authority and evidence bundles. Revision must use the
pinned anchor/patch/apply/roadmap contracts (including refusal/escalation and
human checkpoints), not a wholesale rewrite as a shortcut. Never invent sources,
DOIs, experiments, human approval, review independence or gate results.
