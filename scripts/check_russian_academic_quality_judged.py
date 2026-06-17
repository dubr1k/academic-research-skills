#!/usr/bin/env python3
"""Deterministic judged-output checker for Russian academic quality evals.

The checker scores recorded `model_output` text against rubric markers and can
optionally validate cached judge verdict fixtures over captured candidate
outputs. Cached verdicts add dimension-level metrics without requiring live LLM
calls in CI.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_DIR = REPO_ROOT / "evals/gold/russian_academic_quality_judged"
DEFAULT_GOLD_SET = DEFAULT_EVAL_DIR / "gold_set.json"
DEFAULT_CANDIDATE_MANIFEST = DEFAULT_EVAL_DIR / "candidate_outputs/baseline/manifest.json"

EXPECTED_LABEL_SUPPORT: dict[str, int] = {
    "gost_bibliography": 1,
    "vak_rinc_status": 1,
    "source_verification": 1,
    "russian_style": 1,
    "revision_traceability": 1,
    "mixed_language_routing": 1,
}

VERDICT_VALUES = {"pass", "fail", "needs_human_review"}
DIMENSION_VALUES = {"pass", "fail", "needs_human_review"}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def _contains(text: str, term: str) -> bool:
    return _norm(term) in _norm(text)


def _load_gold_set(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("items"), list):
        raise ValueError("gold set must contain an items[] list")
    return data


def _load_candidate_manifest(path: Path = DEFAULT_CANDIDATE_MANIFEST) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    outputs = data.get("outputs")
    if not isinstance(outputs, list):
        raise ValueError("candidate manifest must contain outputs[]")
    return {entry["id"]: entry for entry in outputs}


def _load_cached_verdicts(verdict_dir: Path | None) -> dict[str, dict[str, Any]]:
    if verdict_dir is None:
        return {}
    if not verdict_dir.is_dir():
        raise ValueError(f"judge verdict directory not found: {verdict_dir}")

    candidate_by_id = _load_candidate_manifest()
    verdicts: dict[str, dict[str, Any]] = {}
    for path in sorted(verdict_dir.glob("*.json")):
        verdict = json.loads(path.read_text(encoding="utf-8"))
        case_id = verdict.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{path.name}: missing non-empty case_id")
        candidate = candidate_by_id.get(case_id)
        if candidate is None:
            raise ValueError(f"{path.name}: case_id {case_id!r} not found in candidate manifest")
        verdict["_expected_candidate"] = candidate
        verdicts[case_id] = verdict
    return verdicts


def _validate_cached_verdict(item_id: str, verdict: dict[str, Any]) -> tuple[list[str], bool, int, int, bool]:
    errors: list[str] = []
    expected = verdict["_expected_candidate"]

    verdict_value = verdict.get("verdict")
    if verdict_value not in VERDICT_VALUES:
        errors.append(f"{item_id}: invalid cached judge verdict {verdict_value!r}")

    if verdict.get("candidate_path") != expected["path"]:
        errors.append(f"{item_id}: candidate_path drift in cached judge verdict")
    if verdict.get("candidate_sha256") != expected["sha256"]:
        errors.append(f"{item_id}: candidate_sha256 drift in cached judge verdict")

    dimension_results = verdict.get("dimension_results")
    if not isinstance(dimension_results, dict) or not dimension_results:
        errors.append(f"{item_id}: dimension_results must be a non-empty object")
        passed_dimensions = 0
        total_dimensions = 0
    else:
        invalid = {
            key: value for key, value in dimension_results.items()
            if value not in DIMENSION_VALUES
        }
        if invalid:
            errors.append(f"{item_id}: invalid dimension_results values: {invalid}")
        passed_dimensions = sum(1 for value in dimension_results.values() if value == "pass")
        total_dimensions = len(dimension_results)

    hard_failures = verdict.get("hard_failures")
    if not isinstance(hard_failures, list):
        errors.append(f"{item_id}: hard_failures must be a list")
        has_hard_failure = True
    else:
        has_hard_failure = bool(hard_failures)

    if not isinstance(verdict.get("rationale"), str) or not verdict["rationale"].strip():
        errors.append(f"{item_id}: rationale must be non-empty")
    evidence_quotes = verdict.get("evidence_quotes")
    if not isinstance(evidence_quotes, list) or not evidence_quotes:
        errors.append(f"{item_id}: evidence_quotes must be a non-empty list")

    cached_pass = (
        verdict_value == "pass"
        and not has_hard_failure
        and total_dimensions > 0
        and passed_dimensions == total_dimensions
    )
    needs_human_review = (
        verdict_value == "needs_human_review"
        or (isinstance(dimension_results, dict)
            and any(value == "needs_human_review" for value in dimension_results.values()))
    )
    if needs_human_review:
        errors.append(f"{item_id}: needs_human_review is not a pass")

    return errors, cached_pass, passed_dimensions, total_dimensions, needs_human_review


def evaluate_items(items: list[dict[str, Any]],
                   cached_verdicts: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    errors: list[str] = []
    item_results: list[dict[str, Any]] = []
    per_label_counts: dict[str, dict[str, int]] = {
        label: {"support": 0, "passed": 0, "critical_failures": 0}
        for label in EXPECTED_LABEL_SUPPORT
    }
    passed_items = 0
    critical_failures = 0
    dimension_passed = 0
    dimension_total = 0
    needs_human_review_count = 0
    cached_verdicts = cached_verdicts or {}

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
        marker_passed = not missing_markers and not forbidden_markers

        cached_verdict = cached_verdicts.get(item_id)
        cached_passed = True
        cached_result: dict[str, Any] | None = None
        if cached_verdict is not None:
            (
                verdict_errors,
                cached_passed,
                verdict_dimensions_passed,
                verdict_dimensions_total,
                needs_human_review,
            ) = _validate_cached_verdict(item_id, cached_verdict)
            errors.extend(verdict_errors)
            dimension_passed += verdict_dimensions_passed
            dimension_total += verdict_dimensions_total
            if needs_human_review:
                needs_human_review_count += 1
            cached_result = {
                key: value for key, value in cached_verdict.items()
                if not key.startswith("_")
            }

        passed = marker_passed and cached_passed

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
            "cached_judge_verdict": cached_result,
        })

    total = len(items)
    judged_pass_rate = passed_items / total if total else 0.0
    critical_failure_rate = critical_failures / total if total else 0.0
    dimension_pass_rate = dimension_passed / dimension_total if dimension_total else 1.0
    needs_human_review_rate = needs_human_review_count / total if total else 0.0

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
            "dimension_pass_rate": dimension_pass_rate,
            "needs_human_review_rate": needs_human_review_rate,
        },
        "item_results": item_results,
        "per_label": per_label,
        "errors": errors,
    }


def validate_gold_set(path: Path = DEFAULT_GOLD_SET,
                      verdict_dir: Path | None = None) -> dict[str, Any]:
    data = _load_gold_set(path)
    verdicts = _load_cached_verdicts(verdict_dir) if verdict_dir is not None else {}
    return evaluate_items(data["items"], verdicts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("gold_set", nargs="?", type=Path, default=DEFAULT_GOLD_SET)
    parser.add_argument("--verdict-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    result = validate_gold_set(args.gold_set, args.verdict_dir)
    metrics = result["metrics"]
    print(
        "russian_academic_quality_judged: "
        f"judged_pass_rate={metrics['judged_pass_rate']:.3f} "
        f"critical_failure_rate={metrics['critical_failure_rate']:.3f} "
        f"dimension_pass_rate={metrics['dimension_pass_rate']:.3f} "
        f"needs_human_review_rate={metrics['needs_human_review_rate']:.3f}"
    )
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
