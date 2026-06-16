#!/usr/bin/env python3
"""Structural checker for the Russian academic quality advisory gold set.

This checker does not score model prose. It verifies that every Russian
academic quality fixture is gradeable: each case declares expected guards,
forbidden actions, preservation requirements, and label-specific risk anchors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_SET = REPO_ROOT / "evals/gold/russian_academic_quality/gold_set.json"

LABEL_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "gost_bibliography": ("ГОСТ", "metadata_missing"),
    "vak_rinc_status": ("ВАК",),
    "source_verification": ("verification",),
    "russian_style": ("cliche", "Russian academic"),
    "revision_traceability": ("status",),
    "mixed_language_routing": ("source_language",),
}

LABEL_GUARD_TERMS: dict[str, tuple[str, ...]] = {
    "gost_bibliography": ("metadata_missing",),
    "source_verification": ("verify",),
    "russian_style": ("cliche",),
    "revision_traceability": ("status",),
    "mixed_language_routing": ("source_language",),
}

EXPECTED_LABEL_SUPPORT: dict[str, int] = {
    "gost_bibliography": 2,
    "vak_rinc_status": 2,
    "source_verification": 5,
    "russian_style": 2,
    "revision_traceability": 2,
    "mixed_language_routing": 2,
}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def _contains(text: str, term: str) -> bool:
    return _norm(term) in _norm(text)


def _joined(values: Any) -> str:
    if isinstance(values, list):
        return " ".join(str(value) for value in values)
    return str(values or "")


def _load_gold_set(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("items"), list):
        raise ValueError("gold set must contain an items[] list")
    return data


def evaluate_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    item_results: list[dict[str, Any]] = []
    per_label_counts: dict[str, dict[str, int]] = {
        label: {"support": 0, "covered": 0}
        for label in LABEL_REQUIREMENTS
    }
    covered_items = 0
    forbidden_leaks = 0

    for item in items:
        item_id = item.get("id", "<missing-id>")
        label = item.get("label")
        if label not in LABEL_REQUIREMENTS:
            errors.append(f"{item_id}: invalid label {label!r}")
            continue

        prompt = item.get("prompt")
        guards = item.get("expected_guards")
        must_preserve = item.get("must_preserve")
        must_not_do = item.get("must_not_do")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{item_id}: missing non-empty prompt")
            continue
        if not isinstance(guards, list) or not guards:
            errors.append(f"{item_id}: expected_guards must be a non-empty list")
            continue
        if not isinstance(must_preserve, list) or not must_preserve:
            errors.append(f"{item_id}: must_preserve must be a non-empty list")
            continue
        if not isinstance(must_not_do, list) or not must_not_do:
            errors.append(f"{item_id}: must_not_do must be a non-empty list")
            continue

        envelope = " ".join([
            prompt,
            _joined(guards),
            _joined(must_preserve),
            _joined(must_not_do),
        ])
        guard_text = _joined(guards)
        missing_terms = [
            term for term in LABEL_REQUIREMENTS[label]
            if not _contains(envelope, term)
        ]
        missing_guard_terms = [
            term for term in LABEL_GUARD_TERMS.get(label, ())
            if not _contains(guard_text, term)
        ]
        leaked_forbidden = [
            forbidden for forbidden in must_not_do
            if _contains(guard_text, str(forbidden))
        ]

        per_label_counts[label]["support"] += 1
        covered = not missing_terms and not missing_guard_terms
        if covered:
            covered_items += 1
            per_label_counts[label]["covered"] += 1
        if leaked_forbidden:
            forbidden_leaks += 1

        if missing_terms:
            errors.append(f"{item_id}: missing required risk terms: {missing_terms}")
        if missing_guard_terms:
            errors.append(f"{item_id}: missing required guard terms: {missing_guard_terms}")
        if leaked_forbidden:
            errors.append(
                f"{item_id}: expected guards repeat forbidden actions: {leaked_forbidden}"
            )

        item_results.append({
            "id": item_id,
            "label": label,
            "covered": covered,
            "forbidden_action_leak": bool(leaked_forbidden),
        })

    total = len(items)
    advisory_recall = covered_items / total if total else 0.0
    forbidden_action_rate = forbidden_leaks / total if total else 0.0

    per_label = []
    for label, counts in per_label_counts.items():
        support = counts["support"]
        coverage = counts["covered"] / support if support else 0.0
        expected_support = EXPECTED_LABEL_SUPPORT[label]
        if support != expected_support:
            errors.append(f"{label}: expected support {expected_support}, got {support}")
        per_label.append({
            "label": label,
            "support": support,
            "guard_coverage": coverage,
        })

    expected_total = sum(EXPECTED_LABEL_SUPPORT.values())
    if total != expected_total:
        errors.append(f"sample_n must be {expected_total}, got {total}")

    return {
        "metrics": {
            "advisory_recall": advisory_recall,
            "forbidden_action_rate": forbidden_action_rate,
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
        "russian_academic_quality: "
        f"advisory_recall={metrics['advisory_recall']:.3f} "
        f"forbidden_action_rate={metrics['forbidden_action_rate']:.3f}"
    )
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
