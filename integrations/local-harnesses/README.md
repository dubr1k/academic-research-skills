# Local Claude/OpenCode adapters

Build without changing host configuration:

```sh
python3 integrations/local-harnesses/build.py --destination /absolute/new/bundle
python3 -m unittest discover -s integrations/local-harnesses -p 'test_*.py'
```

The bundle preserves committed canonical methodology at its root, eight narrow
entrypoints for Claude and eight for shared discovery, 21 adapted user commands,
the host runtime contract, and source/generated hashes in `HOST-MANIFEST.json`.
Existing destinations and source-tree destinations are refused. No model or
network call is made. Test outputs must be outside the checkout.

After separately backing up existing host installations, point Claude personal
skills at `host-skills/claude`, shared `.agents/skills` at `host-skills/shared`, and
user commands at `host-commands`. Do not also copy the same shared skills into
OpenCode's global skills directory. The two Claude full-cycle skills are explicit
only (`disable-model-invocation: true`). Shared runtimes enforce scope through
the narrow description and runtime contract, not a Claude-only control.

OpenCode can independently discover Claude's account-synced Cowork skills. Use
its supported `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=true` environment switch for
future processes if those should be isolated. oh-my-openagent has its own
`claude_code.skills` setting; set it false and explicitly add `.agents/skills` to
`skills.sources` if shared skills should remain visible in all OMO registries.
Do not delete or rename Claude's synced account files. Configure process startup
outside this builder, and check a new process rather than assuming running
sessions have adopted a changed environment.

These adapters do not change upstream role/methodology content or other host
integrations. Hash differences from raw upstream SKILL.md are expected; the
manifest identifies the exact preserved scientific source.
