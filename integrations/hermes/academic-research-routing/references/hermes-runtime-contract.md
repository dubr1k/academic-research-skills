# Hermes execution and language adapter

This adapter changes runtime mapping, not the pinned upstream scientific method. Installed source provenance and hashes are in `../academic-suite/HERMES-INSTALL-MANIFEST.json` relative to the router directory. Resolve the actual router/suite paths from `skill_view`; never use a source checkout under cache/scratch as a dependency.

## Runtime and evidence

- Preserve upstream root-relative layouts. Use `terminal` with the installed suite as `workdir` and explicit absolute passport, records, protocol and output paths. Check Python dependencies against `requirements-dev.txt` before selecting a runtime; do not install or mutate the user's environment silently. Select a project virtual environment with the declared dependencies; do not assume a particular machine-local Python path.
- Main assistant owns substantive final prose; isolated-context delegates provide bounded search, extraction, critique and checks. `Workflow` and `Agent` are foreign orchestration interfaces: use `delegate_task` if available and preserve role-specific contracts. Conversation separation does not prevent shared filesystem or tool access. Never label this OS/tool isolation or claim independent blinded evaluation merely because two roles ran.
- For screening, use the bundled preparation/merge/report scripts; generated JavaScript workflows are not native Hermes executables. Preserve protocol confirmation, pilot, independent reviewer returns, adjudication, QC and pending-state gates. Missing model/worker independence blocks the relevant gate, rather than licensing invented reviewer results.
- Execute `scripts/run_ledger.py --help` to inspect its supported CLI. Persist initial instructions, checkpoint opens/closes and tool receipts when they occur; recover with the real passport and event files, not reconstructed success. Handoff checks must compare expected steps and flag material gaps. A passing deterministic ledger test does not prove that a future model wrote all events.
- Record real exit codes and artifacts. Fixtures verify software contracts, not screening accuracy, scientific validity, publication readiness or actual independent review.

## Output-language boundary

- Record interaction language, manuscript language and requested abstract languages in a separate Hermes adapter note, and carry that instruction into every relevant role.
- Pinned v3.23.0 Phase 1 recognizes only `output_language_pair: zh-tw-en`. It does not support a Russian/English pair token. Never invent or serialize `ru-en`, repurpose Chinese fields as Russian, or claim omission changes the upstream default: omission retains Traditional Chinese/English behavior.
- RU/EN output follows the user's explicit language request through this adapter, not an upstream locale pack. Produce the requested RU/EN text as an explicitly labeled adapter artifact outside the unmodified pair-bound Schema-4 abstract carrier. Do not automatically invoke the default Chinese/English abstract path for that artifact.
- If a required downstream step demands a Schema-4 pair-bound RU/EN payload, stop and report the unsupported contract; obtain an explicit supported alternative. Do not silently normalize unsupported values or weaken upstream validation.

## Verification

From the repository root, run `python -m unittest discover -s integrations/hermes/tests -v`, then the bounded upstream tests listed in `integrations/hermes/README.md`. The portable adapter test checks complete package hashes, the preserved reference, unique discovery, language/routing guard text and an installation into a temporary destination. Local receipts are generated at installation time and are not repository content. These are deterministic checks, not proof of model compliance.

## Updating this installation

1. Pin and verify source commit before copying; inspect changes, dependencies and selected tests.
2. Back up suite, router and bundle before editing; record backup hashes.
3. Compare installed files against the previous pin to detect local changes. Preserve local references and represent overlays separately from upstream hashes.
4. Copy the complete runtime/support closure at its original relative roots. Exclude `skills/` symlink aliases and `integrations/` duplicate skill wrappers so discovery exposes nine methodology skills only. Never leave scratch-checkout dependencies.
5. Keep platform mappings here rather than editing upstream methods. Extend the bundle and explicit screening route without treating every systematic review as screening.
6. Run bounded offline contract tests from the installed root, verify all copied hashes and adapter invariants, and write a provenance manifest plus test report. Disclose skipped tests and untested model behavior. Do not change other profiles, config or remote hosts as part of this workflow.
