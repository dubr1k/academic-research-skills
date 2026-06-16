import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_DOC = ROOT / "docs" / "russian-academic-context.md"

RU_EXAMPLES = {
    "examples/ru/research-gost-vak.md": "akademicheskoe-issledovanie",
    "examples/ru/research-source-verification-depth.md": "akademicheskoe-issledovanie",
    "examples/ru/paper-abstract-gost.md": "akademicheskaya-statya",
    "examples/ru/paper-gost-source-types.md": "akademicheskaya-statya",
    "examples/ru/reviewer-vak-rinc.md": "akademicheskii-retsenzent",
    "examples/ru/reviewer-rereview-traceability.md": "akademicheskii-retsenzent",
    "examples/ru/pipeline-dissertation-to-article.md": "akademicheskii-konveer",
    "examples/bilingual/scopus-apa-russian-prompt.md": "akademicheskaya-statya",
    "examples/bilingual/russian-journal-apa-override.md": "akademicheskaya-statya",
    "examples/bilingual/pipeline-bilingual-handoff.md": "akademicheskii-konveer",
    "examples/bilingual/mixed-corpus-cyberleninka-scopus.md": "akademicheskoe-issledovanie",
    "examples/bilingual/mixed-source-verification-handoff.md": "akademicheskoe-issledovanie",
}


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_russian_academic_context_doc_covers_local_requirements():
    text = read_text(CONTEXT_DOC)

    for required in (
        "ГОСТ Р 7.0.5-2008",
        "ВАК",
        "РИНЦ",
        "eLIBRARY",
        "CyberLeninka",
        "peer_reviewed_verified",
        "partially_verified",
        "metadata_missing",
        "source_language",
        "source_system",
        "traceability table",
    ):
        assert required in text


def test_ru_and_bilingual_examples_route_to_expected_skills():
    for path, expected_skill in RU_EXAMPLES.items():
        text = read_text(ROOT / path)

        assert f"Expected skill: `{expected_skill}`" in text
        assert "Routing:" in text
        assert "Expected checks:" in text


def test_russian_quality_fixtures_are_covered_by_context_doc():
    context = read_text(CONTEXT_DOC)
    cases = json.loads(read_text(ROOT / "tests/fixtures/russian_quality_cases.json"))

    assert len(cases) >= 5
    for case in cases:
        assert case["risk"] in context
        for required_key in ("id", "signal", "expected_guard"):
            assert case[required_key]
