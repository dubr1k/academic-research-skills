"""Tests for the Russian academic quality advisory gold-set checker."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import check_russian_academic_quality as checker


REPO_ROOT = Path(__file__).resolve().parents[1]
GOLD_SET = REPO_ROOT / "evals" / "gold" / "russian_academic_quality" / "gold_set.json"


def test_validate_gold_set_reports_full_advisory_coverage():
    result = checker.validate_gold_set(GOLD_SET)

    assert result["errors"] == []
    assert result["metrics"]["advisory_recall"] == pytest.approx(1.0)
    assert result["metrics"]["forbidden_action_rate"] == pytest.approx(0.0)
    assert len(result["item_results"]) == 12


def test_each_label_has_two_gradeable_cases():
    result = checker.validate_gold_set(GOLD_SET)

    by_label = {entry["label"]: entry for entry in result["per_label"]}
    assert set(by_label) == set(checker.LABEL_REQUIREMENTS)
    assert all(entry["support"] == 2 for entry in by_label.values())
    assert all(entry["guard_coverage"] == pytest.approx(1.0) for entry in by_label.values())


def test_missing_required_guard_term_is_reported(tmp_path):
    data = json.loads(GOLD_SET.read_text(encoding="utf-8"))
    data["items"][0]["expected_guards"] = ["ask for missing fields"]
    path = tmp_path / "gold_set.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = checker.validate_gold_set(path)

    assert result["metrics"]["advisory_recall"] < 1.0
    assert any("missing required guard terms" in error for error in result["errors"])


def test_forbidden_action_leaking_into_guard_is_reported(tmp_path):
    data = json.loads(GOLD_SET.read_text(encoding="utf-8"))
    forbidden = data["items"][0]["must_not_do"][0]
    data["items"][0]["expected_guards"].append(forbidden)
    path = tmp_path / "gold_set.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = checker.validate_gold_set(path)

    assert result["metrics"]["forbidden_action_rate"] > 0.0
    assert any("expected guards repeat forbidden actions" in error for error in result["errors"])
