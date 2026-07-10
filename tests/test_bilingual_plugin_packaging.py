import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SKILLS = {
    "deep-research",
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
    "akademicheskoe-issledovanie",
    "akademicheskaya-statya",
    "akademicheskii-retsenzent",
    "akademicheskii-konveer",
}


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_plugin_skill_bundle_contains_english_and_russian_skills():
    packaged_skills = {
        path.name
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }

    assert packaged_skills == EXPECTED_SKILLS


def test_claude_plugin_metadata_describes_bilingual_bundle():
    plugin = read_json(".claude-plugin/plugin.json")
    marketplace = read_json(".claude-plugin/marketplace.json")

    assert plugin["name"] == "academic-research-skills"
    assert plugin["version"] == "3.15.0"
    assert "Bilingual" in plugin["description"]
    assert "ГОСТ" in plugin["description"]
    assert "ВАК" in plugin["description"]
    assert "bilingual" in plugin["keywords"]

    [entry] = marketplace["plugins"]
    assert entry["name"] == plugin["name"]
    assert entry["version"] == plugin["version"]
    assert "8 skills" in entry["description"]
    assert "/ars-ru-*" in entry["description"]
    assert {Path(path).name for path in entry["skills"]} == EXPECTED_SKILLS
    assert len(entry["skills"]) == 8


def test_codex_plugin_manifest_points_to_bilingual_skills():
    plugin = read_json(".codex-plugin/plugin.json")
    interface = plugin["interface"]

    assert plugin["name"] == "academic-research-skills"
    assert plugin["skills"] == "./skills/"
    assert plugin["version"] == "3.15.0"
    assert "bilingual" in plugin["keywords"]
    assert "ГОСТ" in plugin["description"]
    assert "ВАК" in interface["longDescription"]
    assert len(interface["defaultPrompt"]) == 3
