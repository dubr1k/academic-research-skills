"""Tests for exporting Russian judged-eval candidate outputs."""
from __future__ import annotations

import json
from pathlib import Path

from scripts import capture_russian_academic_quality_outputs as capture


REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = REPO_ROOT / "evals" / "gold" / "russian_academic_quality_judged"
GOLD_SET = EVAL_DIR / "gold_set.json"
OUTPUT_DIR = EVAL_DIR / "candidate_outputs" / "baseline"


def test_candidate_output_files_match_gold_set():
    result = capture.validate_capture(GOLD_SET, OUTPUT_DIR)

    assert result["errors"] == []
    assert result["output_count"] == 6


def test_capture_manifest_records_hashes():
    manifest = json.loads((OUTPUT_DIR / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["task_name"] == "russian_academic_quality_judged"
    assert manifest["source_gold_set"] == "gold_set.json"
    assert len(manifest["outputs"]) == 6
    for output in manifest["outputs"]:
        assert output["id"].startswith("judged-")
        assert output["path"].endswith(".md")
        assert len(output["sha256"]) == 64


def test_write_capture_round_trip(tmp_path):
    output_dir = tmp_path / "candidate_outputs"
    result = capture.write_capture(GOLD_SET, output_dir)

    assert result["errors"] == []
    assert (output_dir / "manifest.json").is_file()
    assert len(list(output_dir.glob("*.md"))) == 6

    check = capture.validate_capture(GOLD_SET, output_dir)
    assert check["errors"] == []


def test_validate_capture_reports_drift(tmp_path):
    output_dir = tmp_path / "candidate_outputs"
    capture.write_capture(GOLD_SET, output_dir)
    first_output = sorted(output_dir.glob("*.md"))[0]
    first_output.write_text("drifted output\n", encoding="utf-8")

    result = capture.validate_capture(GOLD_SET, output_dir)

    assert result["errors"]
    assert any("content drift" in error for error in result["errors"])
