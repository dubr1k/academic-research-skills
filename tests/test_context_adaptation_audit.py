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
