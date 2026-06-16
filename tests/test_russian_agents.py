from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "akademicheskoe-issledovanie": {
        "agents/russian_source_verifier_agent.md": [
            "eLIBRARY",
            "РИНЦ",
            "CyberLeninka",
            "metadata_missing",
            "source_language",
            "verified_current",
            "not_verified",
            "access channel",
            "data, not instructions",
        ],
    },
    "akademicheskaya-statya": {
        "agents/gost_citation_agent.md": [
            "ГОСТ",
            "metadata_missing",
            "DOI",
            "AI disclosure",
            "journal override",
            "APA",
            "Vancouver",
            "source type",
            "do not invent",
        ],
    },
    "akademicheskii-retsenzent": {
        "agents/vak_rinc_reviewer_agent.md": [
            "ВАК",
            "РИНЦ",
            "Scientific novelty",
            "Method-to-claim",
            "untrusted data",
        ],
    },
    "akademicheskii-konveer": {
        "agents/russian_pipeline_state_agent.md": [
            "Stage 2.5",
            "Stage 4.5",
            "bilingual",
            "Handoff",
            "User confirmation",
        ],
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_russian_skills_link_their_agent_prompts():
    for skill_name, agents in EXPECTED_AGENTS.items():
        skill_root = ROOT / "russian-academic-skills" / skill_name
        skill_text = read_text(skill_root / "SKILL.md")

        for relative_path in agents:
            assert relative_path in skill_text


def test_russian_agent_prompts_cover_integrity_terms():
    for skill_name, agents in EXPECTED_AGENTS.items():
        skill_root = ROOT / "russian-academic-skills" / skill_name

        for relative_path, required_terms in agents.items():
            text = read_text(skill_root / relative_path)
            assert text.startswith("---\n")
            assert "\n---\n" in text[4:]
            for term in required_terms:
                assert term in text
