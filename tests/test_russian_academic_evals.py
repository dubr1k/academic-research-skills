import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "evals" / "gold" / "russian_academic_quality"
JUDGED_EVAL_DIR = ROOT / "evals" / "gold" / "russian_academic_quality_judged"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_russian_academic_quality_eval_manifest_declares_scope():
    manifest_path = EVAL_DIR / "manifest.yaml"
    assert manifest_path.exists()

    manifest = yaml.safe_load(read_text(manifest_path))
    assert manifest["task_name"] == "russian_academic_quality"
    assert manifest["task_type"] == "advisory-calibration"
    assert manifest["target"]["gold_set_path"] == "gold_set.json"
    assert manifest["sample_n"] >= 22

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
    assert distribution["gost_bibliography"] >= 5
    assert distribution["vak_rinc_status"] >= 3
    assert distribution["source_verification"] >= 5
    assert distribution["revision_traceability"] >= 4
    assert distribution["mixed_language_routing"] >= 3


def test_russian_academic_quality_gold_set_covers_local_risks():
    gold_path = EVAL_DIR / "gold_set.json"
    assert gold_path.exists()

    gold = json.loads(read_text(gold_path))
    items = gold["items"]
    assert len(items) >= 22
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
    ids = {item["id"] for item in items}
    assert {
        "gost-003-journal-article-source-type",
        "gost-004-web-source-missing-access-date",
        "gost-005-russian-journal-apa-override",
        "vak-003-review-index-quality-separation",
        "source-003-elibrary-rinc-vak",
        "source-004-incomplete-russian-record",
        "source-005-mixed-source-language",
        "trace-003-rereview-page-section-evidence",
        "trace-004-needs-evidence-taxonomy",
        "mixed-003-pipeline-final-package-mode",
    } <= ids

    for required_term in (
        "ГОСТ Р 7.0.5-2008",
        "ВАК",
        "РИНЦ",
        "eLIBRARY",
        "CyberLeninka",
        "DOI",
        "metadata_missing",
        "journal override",
        "journal-index status",
        "needs_evidence",
        "final_package_mode",
        "verified_current",
        "not_verified",
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


def test_russian_academic_quality_judged_eval_manifest_declares_scope():
    manifest_path = JUDGED_EVAL_DIR / "manifest.yaml"
    assert manifest_path.exists()

    manifest = yaml.safe_load(read_text(manifest_path))
    assert manifest["task_name"] == "russian_academic_quality_judged"
    assert manifest["task_type"] == "llm-output-judged"
    assert manifest["target"]["gold_set_path"] == "gold_set.json"
    assert manifest["target"]["predicted_field"] == "model_output"
    assert manifest["sample_n"] == 6

    labels = set(manifest["labels"])
    assert labels == {
        "gost_bibliography",
        "vak_rinc_status",
        "source_verification",
        "russian_style",
        "revision_traceability",
        "mixed_language_routing",
    }


def test_russian_academic_quality_judged_gold_set_scores_outputs():
    gold_path = JUDGED_EVAL_DIR / "gold_set.json"
    assert gold_path.exists()

    gold = json.loads(read_text(gold_path))
    items = gold["items"]
    assert len(items) == 6
    assert len({item["id"] for item in items}) == len(items)

    required_fields = {"id", "label", "prompt", "model_output", "rubric"}
    for item in items:
        assert required_fields <= set(item)
        assert item["model_output"].strip()
        assert item["rubric"]["must_include"]
        assert item["rubric"]["must_avoid"]

    serialized = json.dumps(gold, ensure_ascii=False)
    for required_term in (
        "model_output",
        "must_include",
        "must_avoid",
        "ГОСТ",
        "journal-index status",
        "source_verification_state",
        "needs_evidence",
        "output_language",
    ):
        assert required_term in serialized
