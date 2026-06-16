from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "context-adaptation-audit.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_context_adaptation_audit_exists_and_names_context_axes():
    text = read_text(AUDIT_DOC)

    for required in (
        "# Context Adaptation Audit",
        "English international",
        "Russian journal",
        "ВАК",
        "РИНЦ",
        "eLIBRARY",
        "CyberLeninka",
        "mixed RU/EN",
        "ГОСТ",
        "APA",
        "IEEE",
        "Vancouver",
        "Chicago",
        "source_language",
        "output language",
        "venue",
    ):
        assert required in text


def test_context_adaptation_audit_covers_repo_surfaces():
    text = read_text(AUDIT_DOC)

    for surface in (
        "README.md",
        "README.ru.md",
        "README.en.md",
        "docs/bilingual-routing.md",
        "docs/russian-academic-context.md",
        "docs/skill-parity-matrix.md",
        "docs/upstream-sync.md",
        "commands/",
        "skills/",
        "russian-academic-skills/",
        "agents/",
        "academic-paper/agents/",
        "deep-research/agents/",
        "examples/ru/",
        "examples/bilingual/",
        "evals/gold/russian_academic_quality/",
        "scripts/run_evals.py",
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ):
        assert surface in text


def test_context_adaptation_audit_records_prioritized_backlog():
    text = read_text(AUDIT_DOC)

    for backlog_item in (
        "P3a",
        "P3b",
        "P3c",
        "P3d",
        "Russian source verification",
        "ГОСТ bibliography",
        "ВАК/РИНЦ review",
        "bilingual pipeline handoff",
        "auto/router entrypoint",
        "global shared agents",
    ):
        assert backlog_item in text


def test_context_adaptation_audit_marks_p3b_depth_pass_covered():
    text = read_text(AUDIT_DOC)

    for required in (
        "Status: covered in the first depth pass.",
        "examples/ru/research-source-verification-depth.md",
        "examples/bilingual/mixed-source-verification-handoff.md",
        "verified_current",
        "not_verified",
    ):
        assert required in text


def test_context_adaptation_audit_marks_p3c_depth_pass_covered():
    text = read_text(AUDIT_DOC)

    for required in (
        "P3c: ГОСТ Bibliography and Journal Override Depth",
        "examples/ru/paper-gost-source-types.md",
        "examples/bilingual/russian-journal-apa-override.md",
        "journal article, monograph, dissertation abstract, conference paper, web source",
        "APA, IEEE, Vancouver, or Chicago",
    ):
        assert required in text


def test_context_adaptation_audit_marks_p3d_p3e_p3f_depth_passes_covered():
    text = read_text(AUDIT_DOC)

    for required in (
        "P3d: ВАК/РИНЦ Review and Re-review Traceability",
        "examples/ru/reviewer-rereview-traceability.md",
        "journal-index status",
        "needs_evidence",
        "P3e: Bilingual Pipeline Handoff and Global Shared Agents",
        "examples/bilingual/pipeline-bilingual-handoff.md",
        "source verification state",
        "final_package_mode",
        "global_agent_norm_risk",
        "P3f: Auto/router Entrypoint",
        "commands/ars-auto.md",
        "selected_skill",
    ):
        assert required in text
