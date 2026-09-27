# OpenClaw Research adapter

Four OpenClaw-native skills expose the repository's English and Russian procedures to the `research` agent:

| Installed skill | ARS sources |
| --- | --- |
| `ars-research` | `deep-research`, `akademicheskoe-issledovanie` |
| `ars-paper` | `academic-paper`, `akademicheskaya-statya` |
| `ars-review` | `academic-paper-reviewer`, `akademicheskii-retsenzent` |
| `ars-pipeline` | `academic-pipeline`, `akademicheskii-konveer` |

These are adapters, not copies of the upstream execution harness. They select and read the original procedures, replace unsupported Claude Code `@agent` and OpenCode `task()` orchestration with bounded OpenClaw work, preserve evidence and phase boundaries, and disclose unsupported gates. They require no Anthropic key, Claude Code, or MCP server for the supported prompt-driven workflows. Optional upstream scripts/hooks are not installed or enabled.

For this installation, copy the four `skills/ars-*/` directories into the Research workspace's `skills/` directory, append their four names to `agents.entries.research.skills`, and set the canonical repository path in the Research workspace's `AGENTS.md`. Use `openclaw skills check --agent research`, `openclaw config validate`, and a live `openclaw agent --agent research` smoke test to verify. Repeat the copy and checks after updating this adapter's source.

Source license: CC BY-NC 4.0; upstream Cheng-I Wu, Russian adaptation dubr1k. Check licensing before commercial reuse.
