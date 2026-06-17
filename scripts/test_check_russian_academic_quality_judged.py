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


def test_validate_gold_set_scores_recorded_outputs():
    result = checker.validate_gold_set(GOLD_SET)

    assert result["errors"] == []
    assert result["metrics"]["judged_pass_rate"] == pytest.approx(1.0)
    assert result["metrics"]["critical_failure_rate"] == pytest.approx(0.0)
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
