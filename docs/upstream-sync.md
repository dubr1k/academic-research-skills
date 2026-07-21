# Upstream Sync Workflow

This fork keeps the English upstream package close to `Imbad0202/academic-research-skills` and maintains `russian-academic-skills/` as a Russian adapter layer.

## Remote Layout

- `origin`: this bilingual fork.
- `upstream`: `https://github.com/Imbad0202/academic-research-skills`.

If `upstream` is missing, add it:

```bash
git remote add upstream https://github.com/Imbad0202/academic-research-skills
git fetch upstream
```

## Sync Steps

1. Fetch both remotes:

   ```bash
   git fetch origin
   git fetch upstream
   ```

2. Inspect the upstream diff before merging:

   ```bash
   git diff main..upstream/main -- deep-research academic-paper academic-paper-reviewer academic-pipeline shared agents commands scripts evals tests
   ```

3. Merge or cherry-pick upstream changes into the English core only:

   ```bash
   git merge upstream/main
   ```

4. Resolve conflicts without translating upstream files in place. Keep Russian adaptation changes under `russian-academic-skills/`, `docs/`, bilingual README files, fixtures, and tests.

5. Update the Russian adapter snapshot metadata after the upstream merge is accepted:

   - set `upstream_snapshot` in every Russian `SKILL.md` to the exact upstream commit hash;
   - set `upstream_version` and `upstream_date` from the tracked release/head;
   - update the visible `Upstream snapshot:` line in every Russian `SKILL.md`;
   - refresh `README.en.md` from the same upstream commit;
   - update root/Russian snapshot badges and both plugin manifest versions;
   - preserve explicit marketplace paths for all four English and four Russian skills;
   - update `docs/skill-parity-matrix.md` with a feature-by-feature adaptation decision.

## Russian Adapter Review

After each upstream sync, check whether upstream changes affect:

- research modes, source verification, or integrity gates;
- paper-writing modes, disclosure, citation, or format conversion;
- reviewer decision logic and re-review gates;
- pipeline stage ordering, checkpoints, or handoff contracts;
- command entrypoints and mode registry references.

Do not copy upstream features into Russian skills mechanically. Adapt only the parts that still make sense for ГОСТ, ВАК, РИНЦ/eLIBRARY, CyberLeninka, Russian academic style, and bilingual workflows.

## Plugin Packaging

This fork uses one bilingual plugin bundle rather than a separate Russian plugin. The bundle exposes both upstream English skills and Russian adapters through `skills/`.

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` describe the legacy Claude plugin package.
- `.codex-plugin/plugin.json` describes the Codex-compatible plugin package.
- Keep both metadata surfaces aligned on name, version, repository, license, and bilingual scope.
- After adding or removing a skill, update `skills/`, command docs, and plugin packaging tests together.

## Required Tests

Run targeted bilingual checks first:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/test_bilingual_docs.py tests/test_russian_entrypoints.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/test_bilingual_plugin_packaging.py
python scripts/check_version_consistency.py
python scripts/check_spec_consistency.py
python scripts/check_setup_cross_model_parity.py
python tools/release-discipline/scripts/check_command_invariants.py --manifest .command-invariants.toml
```

Then run every test file listed by the CI pytest manifest and the full suite. If globally installed pytest plugins conflict with the repository, keep `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`; do not change project dependencies merely to satisfy an unrelated external plugin.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
```

Before committing, verify:

- all Russian `SKILL.md` files expose the required frontmatter fields;
- all `/ars-ru-*` commands exist and point to the correct Russian skills;
- bilingual routing fixtures still match `docs/bilingual-routing.md`;
- upstream snapshot metadata is consistent across Russian skills.
