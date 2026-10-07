from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_ROOT = ROOT / "russian-academic-skills"
SNAPSHOT = "6ab4b03bf70a118a1b3ee7f3263ed9f19031061b"


def read_skill(name: str) -> str:
    return (ADAPTER_ROOT / name / "SKILL.md").read_text(encoding="utf-8")


def test_all_russian_adapters_point_to_current_upstream_snapshot():
    for name in (
        "akademicheskoe-issledovanie",
        "akademicheskaya-statya",
        "akademicheskii-retsenzent",
        "akademicheskii-konveer",
    ):
        text = read_skill(name)
        assert 'version: "3.23.0-ru.1"' in text
        assert 'last_updated: "2026-10-07"' in text
        assert f'upstream_snapshot: "{SNAPSHOT}"' in text
        assert 'upstream_version: "v3.23.0"' in text
        assert 'upstream_date: "2026-10-03"' in text


def test_russian_writing_adapter_preserves_claim_strength_during_revision():
    text = read_skill("akademicheskaya-statya")
    for term in (
        "claim-strength ladder",
        "No silent move",
        "claim-strength token conservation",
        "patch_digest",
    ):
        assert term in text


def test_russian_reviewer_adapter_carries_v3_19_review_contracts():
    text = read_skill("akademicheskii-retsenzent")
    for term in (
        "eligible_roles",
        "owner_role",
        "typed evidence anchor",
        "Coverage Receipt",
        "Phase 1",
        "Phase 2A",
        "Phase 2B",
        "persuasion-blind",
        "adjustment record",
        "FULLY_ADDRESSED|PARTIALLY_ADDRESSED|NOT_ADDRESSED|MADE_WORSE|CANNOT_VERIFY",
    ):
        assert term in text
    assert "`needs_evidence`" not in text


def test_russian_reviewer_adapter_preserves_role_scoped_semantics():
    text = read_skill("akademicheskii-retsenzent")
    assert "ineligible dimension" in text
    assert "без `abstain_reason`" in text
    assert "eligible, но неприменимый" in text
    assert "с `abstain_reason`" in text
    assert "явно abstain на остальных" not in text


def test_russian_reviewer_adapter_defines_typed_finding_contract():
    text = read_skill("akademicheskii-retsenzent")
    for term in (
        "text|table|figure|equation|dataset|absence",
        "severity",
        "confidence",
        "competence_basis",
        "Top Blocking Issues",
    ):
        assert term in text
    assert "Reject and Resubmit" not in text


def test_russian_pipeline_adapter_carries_revision_and_re_review_evidence():
    text = read_skill("akademicheskii-konveer")
    for term in (
        "claim-strength ledger",
        "patch_digest",
        "Phase 1",
        "Phase 2A",
        "Phase 2B",
        "user_review_required",
    ):
        assert term in text


def test_russian_pipeline_supporting_assets_carry_stage_3_prime_contract():
    root = ADAPTER_ROOT / "akademicheskii-konveer"
    texts = {
        name: (root / name).read_text(encoding="utf-8")
        for name in (
            "references/bilingual-handoff-contracts.md",
            "agents/russian_pipeline_state_agent.md",
            "templates/pipeline-dashboard.md",
        )
    }
    for text in texts.values():
        for term in (
            "[CONTRACT-ACKNOWLEDGED]",
            "[EVIDENCE-COMMITTED]",
            "[MATRIX-COMMITTED]",
            "patch_digest",
            "user_review_required",
        ):
            assert term in text


def test_russian_adapters_carry_bounded_workflow_profile_binding():
    for name in (
        "akademicheskoe-issledovanie",
        "akademicheskaya-statya",
        "akademicheskii-retsenzent",
        "akademicheskii-konveer",
    ):
        text = read_skill(name)
        assert "research-workflow-profile/1.0" in text
        assert "profile_binding" in text
        assert "content_sha256" in text

    research = read_skill("akademicheskoe-issledovanie")
    for term in (
        "field_general",
        "unresolved_fit",
        "branch_budget",
        "ask_merge_park_archive",
        "authority_points",
    ):
        assert term in research


def test_russian_pipeline_preserves_claim_standing_consent_boundary():
    text = read_skill("akademicheskii-konveer")
    for term in (
        "Claim-Standing Probe",
        "advisory-only",
        "retrieval_plus_stance",
        "transmission ledger",
        "Phase E",
    ):
        assert term in text
    assert "не входит в integrity result" in text


def test_russian_adapters_disclose_install_and_transport_boundaries():
    research = read_skill("akademicheskoe-issledovanie")
    paper = read_skill("akademicheskaya-statya")
    pipeline = read_skill("akademicheskii-konveer")

    for term in ("docs/DATA_FLOWS.md", "docs/CONTROL_AVAILABILITY.md"):
        assert term in pipeline
    for term in ("--classify-content", "STRUCTURE_ONLY", "process-isolated"):
        assert term in research
        assert term in paper
    for term in ("ARS_CROSS_MODEL_TRANSPORT=codex", "citation-integrity"):
        assert term in pipeline
    assert "не для manuscript review" in pipeline
