#!/usr/bin/env python3
"""Deterministic judged-output checker for Russian academic quality evals.

This checker scores recorded model outputs against a small rubric. It is the
first LLM-output eval layer above the structural russian_academic_quality set:
fixtures contain prompts, model_output text, required output markers, and
forbidden critical markers.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_SET = (
    REPO_ROOT
    / "evals/gold/russian_academic_quality_judged/gold_set.json"
)

EXPECTED_LABEL_SUPPORT: dict[str, int] = {
    "gost_bibliography": 1,
    "vak_rinc_status": 1,
    "source_verification": 1,
    "russian_style": 1,
    "revision_traceability": 1,
    "mixed_language_routing": 1,
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def _contains(text: str, term: str) -> bool:
    return _norm(term) in _norm(text)


def _load_gold_set(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("items"), list):
        raise ValueError("gold set must contain an items[] list")
    return data


def evaluate_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    item_results: list[dict[str, Any]] = []
    per_label_counts: dict[str, dict[str, int]] = {
        label: {"support": 0, "passed": 0, "critical_failures": 0}
        for label in EXPECTED_LABEL_SUPPORT
    }
    passed_items = 0
    critical_failures = 0

    for item in items:
        item_id = item.get("id", "<missing-id>")
        label = item.get("label")
        if label not in EXPECTED_LABEL_SUPPORT:
            errors.append(f"{item_id}: invalid label {label!r}")
            continue

        prompt = item.get("prompt")
        model_output = item.get("model_output")
        rubric = item.get("rubric")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{item_id}: missing non-empty prompt")
            continue
        if not isinstance(model_output, str) or not model_output.strip():
            errors.append(f"{item_id}: missing non-empty model_output")
            continue
        if not isinstance(rubric, dict):
            errors.append(f"{item_id}: rubric must be an object")
            continue

        must_include = rubric.get("must_include")
        must_avoid = rubric.get("must_avoid")
        if not isinstance(must_include, list) or not must_include:
            errors.append(f"{item_id}: rubric.must_include must be a non-empty list")
            continue
        if not isinstance(must_avoid, list) or not must_avoid:
            errors.append(f"{item_id}: rubric.must_avoid must be a non-empty list")
            continue

        missing_markers = [
            marker for marker in must_include
            if not _contains(model_output, str(marker))
        ]
        forbidden_markers = [
            marker for marker in must_avoid
            if _contains(model_output, str(marker))
        ]
        passed = not missing_markers and not forbidden_markers

        per_label_counts[label]["support"] += 1
        if passed:
            passed_items += 1
            per_label_counts[label]["passed"] += 1
        if forbidden_markers:
            critical_failures += 1
            per_label_counts[label]["critical_failures"] += 1

        if missing_markers:
            errors.append(
                f"{item_id}: missing required output markers: {missing_markers}"
            )
        if forbidden_markers:
            errors.append(
                f"{item_id}: contains forbidden output markers: {forbidden_markers}"
            )

        item_results.append({
            "id": item_id,
            "label": label,
            "passed": passed,
            "missing_required_markers": missing_markers,
            "forbidden_output_markers": forbidden_markers,
        })

    total = len(items)
    judged_pass_rate = passed_items / total if total else 0.0
    critical_failure_rate = critical_failures / total if total else 0.0

    per_label = []
    for label, counts in per_label_counts.items():
        support = counts["support"]
        expected_support = EXPECTED_LABEL_SUPPORT[label]
        if support != expected_support:
            errors.append(f"{label}: expected support {expected_support}, got {support}")
        per_label.append({
            "label": label,
            "support": support,
            "judged_pass_rate": counts["passed"] / support if support else 0.0,
            "critical_failure_rate": (
                counts["critical_failures"] / support if support else 0.0
            ),
        })

    expected_total = sum(EXPECTED_LABEL_SUPPORT.values())
    if total != expected_total:
        errors.append(f"sample_n must be {expected_total}, got {total}")

    return {
        "metrics": {
            "judged_pass_rate": judged_pass_rate,
            "critical_failure_rate": critical_failure_rate,
        },
        "item_results": item_results,
        "per_label": per_label,
        "errors": errors,
    }


def validate_gold_set(path: Path = DEFAULT_GOLD_SET) -> dict[str, Any]:
    data = _load_gold_set(path)
    return evaluate_items(data["items"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("gold_set", nargs="?", type=Path, default=DEFAULT_GOLD_SET)
    args = parser.parse_args(argv)

    result = validate_gold_set(args.gold_set)
    metrics = result["metrics"]
    print(
        "russian_academic_quality_judged: "
        f"judged_pass_rate={metrics['judged_pass_rate']:.3f} "
        f"critical_failure_rate={metrics['critical_failure_rate']:.3f}"
    )
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
