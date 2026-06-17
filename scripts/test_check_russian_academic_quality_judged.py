"""Tests for the Russian academic quality judged-output gold-set checker."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import check_russian_academic_quality_judged as checker


REPO_ROOT = Path(__file__).resolve().parents[1]
GOLD_SET = (
    REPO_ROOT
    / "evals"
    / "gold"
    / "russian_academic_quality_judged"
    / "gold_set.json"
)
VERDICT_DIR = (
    REPO_ROOT
    / "evals"
    / "gold"
    / "russian_academic_quality_judged"
    / "judge_verdicts"
    / "baseline"
)
CALIBRATION_VERDICT_DIR = (
    REPO_ROOT
    / "evals"
    / "gold"
    / "russian_academic_quality_judged"
    / "judge_verdicts"
    / "calibration"
)


def test_validate_gold_set_scores_recorded_outputs():
    result = checker.validate_gold_set(GOLD_SET)

    assert result["errors"] == []
    assert result["metrics"]["judged_pass_rate"] == pytest.approx(1.0)
    assert result["metrics"]["critical_failure_rate"] == pytest.approx(0.0)
    assert result["metrics"]["dimension_pass_rate"] == pytest.approx(1.0)
    assert result["metrics"]["needs_human_review_rate"] == pytest.approx(0.0)
    assert len(result["item_results"]) == 6


def test_each_label_has_one_judged_output_case():
    result = checker.validate_gold_set(GOLD_SET)

    by_label = {entry["label"]: entry for entry in result["per_label"]}
    assert set(by_label) == set(checker.EXPECTED_LABEL_SUPPORT)
    assert all(entry["support"] == 1 for entry in by_label.values())
    assert all(entry["judged_pass_rate"] == pytest.approx(1.0) for entry in by_label.values())


def test_missing_required_output_marker_is_reported(tmp_path):
    data = json.loads(GOLD_SET.read_text(encoding="utf-8"))
    data["items"][0]["model_output"] = "Попросить требования журнала и не выдумывать DOI."
    path = tmp_path / "gold_set.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = checker.validate_gold_set(path)

    assert result["metrics"]["judged_pass_rate"] < 1.0
    assert any("missing required output markers" in error for error in result["errors"])


def test_forbidden_output_marker_is_reported(tmp_path):
    data = json.loads(GOLD_SET.read_text(encoding="utf-8"))
    forbidden = data["items"][0]["rubric"]["must_avoid"][0]
    data["items"][0]["model_output"] += f" {forbidden}"
    path = tmp_path / "gold_set.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = checker.validate_gold_set(path)

    assert result["metrics"]["critical_failure_rate"] > 0.0
    assert any("contains forbidden output markers" in error for error in result["errors"])


def test_cached_judge_verdicts_are_loaded_and_scored():
    result = checker.validate_gold_set(GOLD_SET, VERDICT_DIR)

    assert result["errors"] == []
    assert result["metrics"]["judged_pass_rate"] == pytest.approx(1.0)
    assert result["metrics"]["dimension_pass_rate"] == pytest.approx(1.0)
    assert result["metrics"]["needs_human_review_rate"] == pytest.approx(0.0)

    for item in result["item_results"]:
        verdict = item["cached_judge_verdict"]
        assert verdict["verdict"] == "pass"
        assert verdict["hard_failures"] == []
        assert set(verdict["dimension_results"].values()) == {"pass"}


def test_cached_judge_verdict_hash_drift_is_reported(tmp_path):
    source = json.loads((VERDICT_DIR / "judged-gost-001.json").read_text(encoding="utf-8"))
    source["candidate_sha256"] = "0" * 64
    verdict_dir = tmp_path / "verdicts"
    verdict_dir.mkdir()
    for path in VERDICT_DIR.glob("*.json"):
        target = verdict_dir / path.name
        if path.name == "judged-gost-001.json":
            target.write_text(json.dumps(source), encoding="utf-8")
        else:
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    result = checker.validate_gold_set(GOLD_SET, verdict_dir)

    assert result["errors"]
    assert any("candidate_sha256 drift" in error for error in result["errors"])


def test_needs_human_review_is_not_a_pass(tmp_path):
    verdict_dir = tmp_path / "verdicts"
    verdict_dir.mkdir()
    for path in VERDICT_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "judged-style-001.json":
            data["verdict"] = "needs_human_review"
            data["dimension_results"]["style_quality"] = "needs_human_review"
        (verdict_dir / path.name).write_text(json.dumps(data), encoding="utf-8")

    result = checker.validate_gold_set(GOLD_SET, verdict_dir)

    assert result["metrics"]["judged_pass_rate"] < 1.0
    assert result["metrics"]["needs_human_review_rate"] > 0.0
    assert any("needs_human_review is not a pass" in error for error in result["errors"])


def test_calibration_verdicts_cover_negative_and_human_review_cases():
    result = checker.validate_gold_set(GOLD_SET, CALIBRATION_VERDICT_DIR)

    assert result["errors"]
    assert result["metrics"]["judged_pass_rate"] < 1.0
    assert result["metrics"]["dimension_pass_rate"] < 1.0
    assert result["metrics"]["needs_human_review_rate"] > 0.0
    assert any("fabricated_source_verification" in error for error in result["errors"])
    assert any("needs_human_review is not a pass" in error for error in result["errors"])

    verdicts = {
        item["id"]: item["cached_judge_verdict"]
        for item in result["item_results"]
    }
    assert any(verdict["verdict"] == "fail" for verdict in verdicts.values())
    assert any(
        verdict["verdict"] == "needs_human_review"
        or "needs_human_review" in verdict["dimension_results"].values()
        for verdict in verdicts.values()
    )
