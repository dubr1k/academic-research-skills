import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "evals" / "gold" / "russian_academic_quality"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_russian_academic_quality_eval_manifest_declares_scope():
    manifest_path = EVAL_DIR / "manifest.yaml"
    assert manifest_path.exists()

    manifest = yaml.safe_load(read_text(manifest_path))
    assert manifest["task_name"] == "russian_academic_quality"
    assert manifest["task_type"] == "advisory-calibration"
    assert manifest["target"]["gold_set_path"] == "gold_set.json"
    assert manifest["sample_n"] >= 12

    labels = set(manifest["labels"])
    assert labels == {
        "gost_bibliography",
        "vak_rinc_status",
        "source_verification",
        "russian_style",
        "revision_traceability",
        "mixed_language_routing",
    }

    distribution = {row["label"]: row["n"] for row in manifest["tuple_distribution"]}
    assert set(distribution) == labels
    assert sum(distribution.values()) == manifest["sample_n"]
    assert all(count >= 2 for count in distribution.values())


def test_russian_academic_quality_gold_set_covers_local_risks():
    gold_path = EVAL_DIR / "gold_set.json"
    assert gold_path.exists()

    gold = json.loads(read_text(gold_path))
    items = gold["items"]
    assert len(items) >= 12
    assert len({item["id"] for item in items}) == len(items)

    required_fields = {
        "id",
        "label",
        "prompt",
        "expected_skill",
        "expected_guards",
        "must_preserve",
        "must_not_do",
    }
    for item in items:
        assert required_fields <= set(item)
        assert item["expected_guards"]
        assert item["must_not_do"]

    serialized = json.dumps(gold, ensure_ascii=False)
    for required_term in (
        "ГОСТ Р 7.0.5-2008",
        "ВАК",
        "РИНЦ",
        "eLIBRARY",
        "CyberLeninka",
        "DOI",
        "metadata_missing",
        "traceability",
        "source_language",
    ):
        assert required_term in serialized


def test_russian_academic_quality_eval_is_documented():
    readme = read_text(EVAL_DIR / "README.md")
    for required_term in (
        "Russian Academic Quality Gold Set",
        "ГОСТ",
        "ВАК/РИНЦ",
        "eLIBRARY",
        "CyberLeninka",
        "traceability",
    ):
        assert required_term in readme
