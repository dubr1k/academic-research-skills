import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_root_readme_links_bilingual_entrypoints():
    readme = read_text("README.md")

    assert readme.startswith("# Двуязычный форк Academic Research Skills")
    assert "## Выбор языка" in readme
    assert "## Наборы навыков" in readme
    assert "## Правило маршрутизации" in readme
    assert "# Academic Research Skills Bilingual Fork" not in readme
    assert "This fork keeps the original English Academic Research Skills package" not in readme
    assert "README.en.md" in readme
    assert "README.ru.md" in readme
    assert "docs/bilingual-routing.md" in readme
    assert "docs/skill-parity-matrix.md" in readme
    assert "docs/context-adaptation-audit.md" in readme


def test_language_specific_readmes_exist():
    english = read_text("README.en.md")
    russian = read_text("README.ru.md")

    assert "# Academic Research Skills for Claude Code" in english
    assert "# Русские академические навыки" in russian


def test_bilingual_routing_fixtures_are_documented():
    routing_doc = read_text("docs/bilingual-routing.md")
    cases = json.loads(read_text("tests/fixtures/bilingual_routing_cases.json"))

    assert len(cases) >= 10
    for case in cases:
        assert case["request"] in routing_doc
        assert f"`{case['expected_skill']}`" in routing_doc


def test_parity_matrix_covers_all_skill_pairs():
    matrix = read_text("docs/skill-parity-matrix.md")

    expected_pairs = {
        "deep-research": "akademicheskoe-issledovanie",
        "academic-paper": "akademicheskaya-statya",
        "academic-paper-reviewer": "akademicheskii-retsenzent",
        "academic-pipeline": "akademicheskii-konveer",
    }

    for upstream, russian in expected_pairs.items():
        assert f"`{upstream}`" in matrix
        assert f"`{russian}`" in matrix


def test_russian_skills_keep_upstream_attribution():
    skill_paths = sorted((ROOT / "russian-academic-skills").glob("*/SKILL.md"))

    assert len(skill_paths) == 4
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        assert "https://github.com/imbad0202/academic-research-skills" in text.lower()
        assert "ad0a7759cee9e7d2db5ca7ea1666096dea8e5d3c" in text
        assert "v3.15.0" in text
        assert "Creative Commons Attribution-NonCommercial 4.0 International" in text


def test_v315_features_are_adapted_across_all_four_russian_skills():
    research = read_text("russian-academic-skills/akademicheskoe-issledovanie/SKILL.md")
    paper = read_text("russian-academic-skills/akademicheskaya-statya/SKILL.md")
    reviewer = read_text("russian-academic-skills/akademicheskii-retsenzent/SKILL.md")
    pipeline = read_text("russian-academic-skills/akademicheskii-konveer/SKILL.md")

    assert "Adjacent-framing probe (v3.15)" in research
    assert "OPENALEX_API_KEY" in research
    assert "budget" in research and "429" in research
    assert "write-scope guard (v3.15)" in paper
    assert "post-task diff" in paper
    assert "write-scope guard" in reviewer and "READ-ONLY" in reviewer
    assert "write_scope_guard: active|inactive|unsupported" in pipeline
    assert "Stage 2.5/4.5" in pipeline
