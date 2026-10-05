# DSH native adapter — experimental, offline-tested

Eight same-name EN/RU skill overlays; core Claude Code/OpenCode sources remain
unchanged. The wrappers apply [HOST.md](HOST.md) to selected domain references,
not a duplicated copy of the large skills. This is not a recognized upstream
port or a claim that a full academic pipeline has passed on DSH.

## Install / update

Python 3.9+ and Git are required. No package installs, network fetches, bootstrap,
hooks, model configuration or changes to other hosts are performed.
Run from the repository root after reviewing and committing the adapter:

```sh
python3 integrations/dsh/install.py --skills-dir "$HOME/.dsh/skills" --dry-run
# Existing copied skills cause a refusal. After inspecting the conflicts:
python3 integrations/dsh/install.py --skills-dir "$HOME/.dsh/skills" --backup --dry-run
python3 integrations/dsh/install.py --skills-dir "$HOME/.dsh/skills" --backup
```

Explicit `--skills-dir` wins; otherwise a nonempty `DSH_HOME` selects
`$DSH_HOME/skills`, falling back to `~/.dsh/skills`. The examples explicitly select
the standard home; omit `--skills-dir` to honor a custom profile home.
`--revision` defaults to local HEAD,
resolved once to a full commit SHA (no fetch). Prefer an explicit reviewed SHA
for reproducibility. Uncommitted domain edits are NOT installed. The adapter
itself runs from the working tree; review/commit it first for attributable
installation. Generated files carry content hashes as well as source commit.

The installer creates:

- Eight immediate child directories, each with SKILL.md, preflight.py and a
  management manifest. Descriptions are DSH-specific, without foreign tool/model
  frontmatter. English and Russian names are unchanged.
- `.ars-dsh/sources/<SHA>/`: complete local `git archive` snapshot (~38 MB at the
  tested base), including scripts, shared contracts, compliance agent/protocol,
  EN/RU references and licenses. Safe in-tree symlinks are preserved. Absolute
  resource paths point here; deleting/moving the original clone does not break
  this snapshot. Moving the installed skills directory does require reinstall.
- `.ars-dsh/backups/`: differing prior skill directories preserved by rename
  only when `--backup` is explicit. **No SKILL.md directly in `.ars-dsh`**: DSH's
  immediate-child discovery must not expose snapshot/backup skills. The automated
  tests assert eight immediate skill entries before and after backup.

Identical reinstall is a no-op. Differing/unmanaged targets (even extra user
files in a managed overlay) require `--backup`. All conflicts are checked before
installation. Root/home and all repository destinations are refused except the
explicit ignored fixture staging subtree `.context/dsh-installer-tests/<fixture>/`.
Symlink destination components are refused; use a physical path. Changed/unmanaged source
snapshots are refused even with `--backup`. No automatic cleanup or deletion.
Use only one installer at a time: installation is not a multi-directory
transaction or protection against concurrent hostile filesystem changes. If
interrupted, inspect the partial destination; preserve it and use a fresh skills
directory rather than bypassing checks. Old snapshots/backups are retained.

After a new commit, repeat dry-run and then `--backup` to install the new SHA.
To restore an old skill, inspect its printed backup path and manually restore it
with DSH stopped/idle; preserve the current directory first. Do not remove source
snapshots while any overlays or backups still reference them.

## Preflight and gates

```sh
python3 "$HOME/.dsh/skills/academic-paper/preflight.py" \
  --skill-dir "$HOME/.dsh/skills/academic-paper" --mode revision
```

Exit 0 = `baseline_ready`, **not quality-gate PASS**. The report always starts
with `quality_gates: not_run`. It verifies hashes of the pinned tracked tree and
overlay files; contract-bearing modes check `jsonschema` and `yaml` imports.
Lightweight quick/fact-check/socratic/plan/outline/abstract modes do not require
those packages. Export uses `--mode format-convert --format docx|pdf|latex|markdown`;
DOCX/PDF checks Pandoc, PDF also checks for a TeX engine. It does not export files.

Before executing a selected gate, read its code and check its actual imports,
inputs and optional dependencies. Online APIs, native tool availability,
PDF/statistical extensions, credentials and cross-model transports require
separate checks. No automatic dependency installs or claims based on file
presence alone. Missing requirements block the affected step; mandatory integrity
stages 2.5/4.5 and revision contracts cannot be disabled. Compliance resources are
restored, not assumed to be executed or scientifically validated.

## Capability / evidence boundary

| Capability | Status and evidence |
|---|---|
| 8 same-name overlays, paths with spaces, pinned full resource tree | Tested in temporary directories by test_install.py |
| Dry-run, conflicts, backup preservation, idempotence, symlink/path refusal, tamper detection | Automated tests; not concurrent-write hardening |
| Missing Python dependencies / export executables | Injected missing-dependency tests; no installation |
| Reviewer role contract + revision patch discipline | Existing checkers executed offline from installed snapshot |
| Native subagent/subagent_fork/send_message mapping | Prompt contract matches available DSH call shapes; no agent-run E2E evidence in this adapter |
| Blind reviewer | Fresh nonfork prompt packet; NOT filesystem isolation or independent model errors |
| Read-only role / artifact allowlist | Prompt-only; no sandbox enforcement; inspect diffs |
| Per-agent model routing / cross-model verification | Unsupported by native call schema; no invented model selection; external transport unconfigured |
| Claude/OpenCode hooks / YAML tool enforcement | Not installed; write_scope_guard unsupported |
| Full publication cycle, online source verification, exports, calibration | Not tested end-to-end; mode-specific preflight and actual gates still required |
| Lightweight routing / workflow restriction | Explicit host instructions, static presence checked; future model behavior not proven |

`workflow` is only allowed when the user explicitly requests a workflow or large
multi-agent orchestration. Ordinary factual prompts do not trigger a full team.
Source templates and agent cards remain domain references, with the transitive
translation policy in HOST.md; foreign runnable APIs never become native tools.

## Tests and provenance

```sh
python3 -m unittest discover -s integrations/dsh -p 'test_*.py'
python3 -m pytest -q scripts/test_check_role_scoped_contract.py \
  scripts/test_check_390_revision_patch_discipline.py scripts/test_ars_apply_revision_patch.py
```

Installer/preflight use stdlib only. The installed upstream checker smoke tests
and upstream test suite require existing jsonschema/PyYAML/pytest as applicable;
tests do not install them. Temporary installer fixtures live in the ignored
`.context/dsh-installer-tests/` staging subtree and are cleaned by unittest;
no real home skill installation is part of tests.
See [TESTING.md](TESTING.md) for the recorded baseline and results.

Source: [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills),
Russian fork [dubr1k/academic-research-skills](https://github.com/dubr1k/academic-research-skills).
Copyright (c) 2026 Cheng-I Wu, CC BY-NC 4.0; [LICENSE](../../LICENSE),
[NOTICE.md](../../NOTICE.md), [THIRD_PARTY.md](../../THIRD_PARTY.md) retained in
snapshots. This adaptation changes host routing/installation only. Update policy:
re-review HOST.md and mode names against the new pinned commit, rerun these tests,
then reinstall explicitly. No automatic updates. Upstream port recognition still
requires maintainer assignment/design review and a real full-pipeline evidence
bundle; this adapter does not claim that work has happened.
