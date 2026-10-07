# Portable Hermes integration

This adapter preserves the repository's public source and license. It packages
methods for Hermes, not Claude/OpenCode/MCP execution. No installed profile,
provider, model, credentials, memory, cron, hooks or services are changed by tests.

## Install a reviewed checkout

Use Python 3.10+ and Git. First inspect the checkout and record `git rev-parse HEAD`.
Choose the actual active profile home; never fall back to another profile.
The destination must be outside the source checkout. Existing skill destinations
are refused, not overwritten: back up and review any existing installation first.

From the repository root, run via the Hermes `terminal` tool:

    python integrations/hermes/install.py --destination "$HERMES_HOME"

The destination is explicit and installation is opt-in. Tests instead install in
an isolated temporary home. Start a new Hermes session afterwards, use `skills_list`
and load the router with `skill_view`. Missing skills are a visible dependency
error, not permission to emulate methods or use an unrelated profile.

## Test

    python -m unittest discover -s integrations/hermes/tests -v

These offline tests exercise packaging and adapter contracts, not model compliance,
scientific validity, live screening accuracy or intervention effectiveness.
Receipts, backups and machine paths are generated locally, never committed here.

## Academic layout and boundaries

Install the complete tracked source under `skills/research/academic-suite`, excluding
`skills/` symlink aliases and `integrations/` duplicate wrappers. Install the router
as a sibling and create a ten-member `skill-bundles/academic.yaml`. A local generated
`HERMES-INSTALL-MANIFEST.json` records hashes and the source commit. Runtime does not
depend on this checkout after installation. Preserve upstream license/source.

The generic applied-business audit reference is carried with the router, unchanged
in meaning (no project examples, company identities or private figures). Load it
for business-material research; upstream methodology files remain byte-identical.

Screening is explicit-only. Generic systematic review/PRISMA does not select
`sr-screener`. Retain pilot, independent reviews, adjudication, QC and pending gates.
Main assistant owns final prose. Delegates are separate contexts, not OS/tool
sandboxes. Missing independence blocks mandatory independent checks.

RU/EN abstracts are labeled adapter artifacts, not invented upstream pair tokens.
The pinned upstream contract supports only `zh-tw-en`; omission retains that default.
Never serialize `ru-en` into its Schema-4 pair carrier. See the runtime contract for
ledger lifecycle, genuine receipts and unsupported-contract handling.

Bounded upstream regression tests (install requirements-dev.txt in a project venv):

    python -m pytest -q tests/test_russian_v3_21_parity.py tests/test_russian_agents.py tests/test_russian_reference_templates.py scripts/test_sr_screener_pipeline.py scripts/test_run_ledger.py scripts/test_evidence_rows.py scripts/test_output_language_pair.py scripts/test_check_routing_core_sync.py scripts/test_excluded_source_entry_schema.py scripts/test_standing_constraint_entry_schema.py

The old machine-specific installation test is intentionally not distributed;
portable tests replace hardcoded backup/interpreter/profile assumptions.
