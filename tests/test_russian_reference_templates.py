from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ASSETS = {
    "akademicheskoe-issledovanie": {
        "references/russian-source-verification.md": [
            "eLIBRARY",
            "РИНЦ",
            "CyberLeninka",
            "peer_reviewed_verified",
            "verified_current",
            "not_verified",
            "metadata_missing",
            "verification ladder",
        ],
        "templates/literature-matrix-gost.md": [
            "Source language",
            "Source system",
            "Current status evidence",
            "ГОСТ Draft Entry",
        ],
    },
    "akademicheskaya-statya": {
        "references/gost-bibliography-guide.md": [
            "ГОСТ",
            "DOI",
            "metadata_missing",
            "journal article",
            "monograph",
            "dissertation abstract",
            "conference paper",
            "web source",
            "journal override",
            "APA",
            "IEEE",
            "Vancouver",
            "Chicago",
        ],
        "templates/vak-article-package.md": [
            "ВАК",
            "Аннотация",
            "Submission Checks",
            "Citation Style Decision",
            "Journal override",
        ],
    },
    "akademicheskii-retsenzent": {
        "references/vak-rinc-review-criteria.md": [
            "ВАК",
            "РИНЦ",
            "scientific novelty",
        ],
        "templates/review-report-traceability.md": [
            "Re-Review Traceability",
            "Original concern",
            "Manuscript evidence",
        ],
    },
    "akademicheskii-konveer": {
        "references/bilingual-handoff-contracts.md": [
            "source_language",
            "source_system",
            "Stage 2.5",
        ],
        "templates/pipeline-dashboard.md": [
            "Russian Academic Pipeline Dashboard",
            "Language And Venue State",
            "Final integrity",
        ],
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_russian_skills_link_their_reference_and_template_assets():
    for skill_name, assets in EXPECTED_ASSETS.items():
        skill_root = ROOT / "russian-academic-skills" / skill_name
        skill_text = read_text(skill_root / "SKILL.md")

        for relative_path in assets:
            assert relative_path in skill_text


def test_russian_reference_and_template_assets_cover_required_terms():
    for skill_name, assets in EXPECTED_ASSETS.items():
        skill_root = ROOT / "russian-academic-skills" / skill_name

        for relative_path, required_terms in assets.items():
            text = read_text(skill_root / relative_path)
            for term in required_terms:
                assert term in text
