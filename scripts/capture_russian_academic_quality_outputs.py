#!/usr/bin/env python3
"""Export and validate Russian judged-eval candidate outputs.

The judged eval keeps recorded `model_output` text in gold_set.json for compact
review. This helper mirrors those outputs into candidate_outputs/<profile>/ so a
future live/cached judge can consume stable files with hash metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_DIR = REPO_ROOT / "evals/gold/russian_academic_quality_judged"
DEFAULT_GOLD_SET = DEFAULT_EVAL_DIR / "gold_set.json"
DEFAULT_OUTPUT_DIR = DEFAULT_EVAL_DIR / "candidate_outputs/baseline"


def _load_gold_set(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("items"), list):
        raise ValueError("gold set must contain an items[] list")
    return data


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    if not slug:
        raise ValueError(f"cannot derive filename from id {value!r}")
    return slug


def _captured_text(item: dict[str, Any]) -> str:
    model_output = item.get("model_output")
    if not isinstance(model_output, str) or not model_output.strip():
        raise ValueError(f"{item.get('id', '<missing-id>')}: missing non-empty model_output")
    return model_output.strip() + "\n"


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _output_entry(item: dict[str, Any], text: str) -> dict[str, Any]:
    item_id = item.get("id")
    label = item.get("label")
    if not isinstance(item_id, str) or not item_id.strip():
        raise ValueError("item missing non-empty id")
    if not isinstance(label, str) or not label.strip():
        raise ValueError(f"{item_id}: missing non-empty label")
    return {
        "id": item_id,
        "label": label,
        "path": f"{_slug(item_id)}.md",
        "sha256": _hash_text(text),
    }


def _build_manifest(gold_set_path: Path, items: list[dict[str, Any]]) -> dict[str, Any]:
    outputs = []
    for item in items:
        outputs.append(_output_entry(item, _captured_text(item)))
    return {
        "task_name": "russian_academic_quality_judged",
        "source_gold_set": gold_set_path.name,
        "output_count": len(outputs),
        "outputs": outputs,
    }


def write_capture(gold_set_path: Path = DEFAULT_GOLD_SET,
                  output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    data = _load_gold_set(gold_set_path)
    items = data["items"]
    output_dir.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []
    manifest = _build_manifest(gold_set_path, items)
    expected_paths = {entry["path"] for entry in manifest["outputs"]}

    for item, entry in zip(items, manifest["outputs"], strict=True):
        text = _captured_text(item)
        (output_dir / entry["path"]).write_text(text, encoding="utf-8")

    for stale in sorted(output_dir.glob("*.md")):
        if stale.name not in expected_paths:
            stale.unlink()

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return {
        "errors": errors,
        "output_count": len(manifest["outputs"]),
        "manifest": manifest,
    }


def validate_capture(gold_set_path: Path = DEFAULT_GOLD_SET,
                     output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    data = _load_gold_set(gold_set_path)
    items = data["items"]
    errors: list[str] = []
    expected_manifest = _build_manifest(gold_set_path, items)

    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        errors.append(f"manifest missing: {manifest_path}")
        actual_manifest: dict[str, Any] = {}
    else:
        actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if actual_manifest != expected_manifest:
            errors.append("manifest drift: manifest.json does not match gold_set.json")

    expected_paths = {entry["path"] for entry in expected_manifest["outputs"]}
    for item, entry in zip(items, expected_manifest["outputs"], strict=True):
        path = output_dir / entry["path"]
        expected_text = _captured_text(item)
        if not path.is_file():
            errors.append(f"candidate output missing: {path}")
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            errors.append(f"{entry['id']}: content drift in {path}")
        actual_hash = _hash_text(actual_text)
        if actual_hash != entry["sha256"]:
            errors.append(f"{entry['id']}: sha256 drift in {path}")

    for extra in sorted(output_dir.glob("*.md")):
        if extra.name not in expected_paths:
            errors.append(f"unexpected candidate output: {extra}")

    return {
        "errors": errors,
        "output_count": len(expected_manifest["outputs"]),
        "manifest": actual_manifest or expected_manifest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold-set", type=Path, default=DEFAULT_GOLD_SET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate existing capture files instead of writing them",
    )
    args = parser.parse_args(argv)

    result = (
        validate_capture(args.gold_set, args.output_dir)
        if args.check
        else write_capture(args.gold_set, args.output_dir)
    )
    action = "check" if args.check else "write"
    print(
        "russian_academic_quality_judged_capture: "
        f"action={action} output_count={result['output_count']}"
    )
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
