from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "version",
    "last_updated",
    "status",
    "data_access_level",
    "task_type",
    "depends_on",
    "upstream_snapshot",
    "upstream_version",
    "upstream_date",
}

RU_COMMANDS = {
    "ars-ru-research.md": "akademicheskoe-issledovanie",
    "ars-ru-paper.md": "akademicheskaya-statya",
    "ars-ru-reviewer.md": "akademicheskii-retsenzent",
    "ars-ru-pipeline.md": "akademicheskii-konveer",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def frontmatter_keys(text: str) -> set[str]:
    assert text.startswith("---\n")
    end = text.index("\n---", 4)
    keys = set()
    for line in text[4:end].splitlines():
        if line and not line.startswith("  ") and ":" in line:
            keys.add(line.split(":", 1)[0])
    return keys


def test_russian_skill_frontmatter_has_required_schema():
    skill_paths = sorted((ROOT / "russian-academic-skills").glob("*/SKILL.md"))

    assert len(skill_paths) == 4
    for path in skill_paths:
        keys = frontmatter_keys(path.read_text(encoding="utf-8"))
        assert keys == REQUIRED_FRONTMATTER_FIELDS


def test_ru_commands_exist_and_route_to_russian_skills():
    for command_file, skill_name in RU_COMMANDS.items():
        command = read_text(f"commands/{command_file}")

        assert f"Trigger the `{skill_name}` skill." in command
        assert f"russian-academic-skills/{skill_name}/SKILL.md" in command
        assert "Do not use this entrypoint" in command
        assert "EN/RU/mixed" in command
        assert "docs/bilingual-routing.md" in command


def test_upstream_sync_doc_covers_required_workflow():
    sync_doc = read_text("docs/upstream-sync.md")

    for required in (
        "origin",
        "upstream",
        "upstream_snapshot",
        "pytest tests/test_bilingual_docs.py tests/test_russian_entrypoints.py",
        "pytest",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
    ):
        assert required in sync_doc
