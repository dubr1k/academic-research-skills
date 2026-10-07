# Recorded offline verification

Source base: `885a3d304d1d55abd715b5f25d07ea63c3401a04` (`origin/main`).
Integration branch: `dsh/native-integration`. Python 3.12 on macOS, existing
jsonschema, PyYAML and pytest available. No package/bootstrap installation.

## Red / green

Before implementation, the first six installer contract tests produced four
expected failures because install.py did not yet exist (two refusal tests already
returned nonzero). This is a missing-feature red baseline, not an upstream defect
reproduction. After implementation: six passed. Added missing-dependency,
installed-checker, compliance-resource and path-safety coverage: eight passed.
A further DSH_HOME regression first failed because the installer ignored the
custom home. After fixing it, nonempty DSH_HOME, explicit CLI precedence and empty
environment fallback are covered by dry-run tests without real-home writes.
Final **nine passed**, 9.419 seconds, exit 0:

```sh
python3 -m unittest discover -s integrations/dsh -p 'test_*.py'
```

These tests install only in ignored `.context/dsh-installer-tests/` temporary
fixtures and clean them. They cover dry-run/no destination writes, exact eight
immediate skill entries, spaces in paths, complete pinned resources, idempotence,
unmanaged and modified targets, backup preservation, symlink/cache rejection,
unsafe root/home/repository descendants (including actual and dry-run `--backup`
against russian-academic-skills), invalid revision/mode, missing module/export
dependencies, overlay/source tampering, and restored compliance-agent hash checks.
Both existing checkers below execute from the INSTALLED snapshot with a working
directory outside the snapshot:

- scripts/check_role_scoped_contract.py — exit 0.
- scripts/check_390_revision_patch_discipline.py — exit 0, eight invariants.

Additional bounded upstream regression run: **143 passed**, 3.19 seconds, exit 0:

```sh
mkdir -p .context/dsh-tests
TMPDIR="$PWD/.context/dsh-tests" python3 -m pytest -q \
  scripts/test_check_role_scoped_contract.py \
  scripts/test_check_390_revision_patch_discipline.py \
  scripts/test_ars_apply_revision_patch.py \
  --basetemp="$PWD/.context/dsh-tests/pytest"
```

One existing pytest-asyncio default-loop-scope deprecation warning; no failures.
No core skill/agent/checker changes. No home skill installation, commits or pushes
performed by this implementation task.

## Not demonstrated

No full publication pipeline, live native-agent academic task, online citation
verification, PDF/DOCX export, cross-model dispatch, human authorization flow or
scientific quality calibration was exercised. Passing prompt/schema/installer
tests is not proof of future model obedience or scientific correctness.
Preflight output explicitly says `baseline_ready` and `quality_gates: not_run`;
selected scripts, inputs, optional extensions and actual gates still need testing
for each real task. Read-only roles remain prompt-only and fresh reviewer context
is not a filesystem sandbox. Parent review/committed-source live install are
separate follow-up steps.
