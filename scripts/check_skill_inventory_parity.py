#!/usr/bin/env python3
"""Lint: the skill inventory is identical on every surface that lists it (#809).

Triage of an external PR that added a fifth top-level skill directory showed
that the existing inventory lints are anchored to the skills they already
know about: `check_spec_consistency.py` hardcodes four SKILL.md paths,
`check_version_consistency.py` iterates the `.claude/CLAUDE.md` table, and
nothing cross-checks the `skills/` symlink directory or the marketplace
manifest. A skill could therefore exist on disk without being packaged,
listed, or versioned, with every lint green.

This fork takes the union of top-level `<name>/SKILL.md` directories and the
explicit localized adapter root `russian-academic-skills/<name>/SKILL.md` as
the authority (it is what exists) and requires set-equality against the three
surfaces that advertise or package the inventory:

  B. `skills/<name>` — one symlink per skill, resolving to its canonical directory
     (plugin auto-discovery packages from here);
  C. `.claude/CLAUDE.md` § "Skills Overview" table rows for the upstream
     top-level skills (localized adapters keep their routing in the bilingual
     plugin/command surfaces so upstream's version lint remains untouched);
  D. `.claude-plugin/marketplace.json` `plugins[].skills[]` as `./<name>` or
     `./russian-academic-skills/<name>`
     (what symlink-blind importers read).

It also checks that any "<N> skills" count claim equals the number of skills
on disk, on the three CURRENT-STATE metadata surfaces that carry one:
`.claude-plugin/plugin.json` description and `marketplace.json` top-level and
per-plugin descriptions. `MODE_REGISTRY.md` is checked against the upstream
table count because Russian adapters reuse those canonical modes rather than
defining a second mode registry. README and CHANGELOG are deliberately out of scope: they
carry historical release notes whose counts are legitimately frozen at the
time of writing, so a prose-wide grep would flag correct history. A surface
that carries no count makes no claim and is not checked.

Every asymmetric difference is reported in both directions, so a stale row
and an unpackaged directory are both single, named violations.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _skill_lint import (
    SKILLS_TABLE_ROW_FULL,
    SKILLS_TABLE_ROW_PREFIX,
    heading_section,
    iter_skill_files,
)

SKILLS_DIR = "skills"
CLAUDE_MD = Path(".claude") / "CLAUDE.md"
MARKETPLACE_JSON = Path(".claude-plugin") / "marketplace.json"
PLUGIN_JSON = Path(".claude-plugin") / "plugin.json"
MODE_REGISTRY_MD = Path("MODE_REGISTRY.md")
LOCALIZED_SKILL_ROOTS = (Path("russian-academic-skills"),)

SKILLS_OVERVIEW_HEADING = "## Skills Overview"
# Row grammar shared with check_version_consistency.py. FULL is what the version
# lint iterates; a row that names a skill but is not FULL is reported here (the
# version lint would silently skip it). PREFIX is kept imported so the shared
# grammar has a visible second consumer.
TABLE_ROW_FULL_RE = re.compile(SKILLS_TABLE_ROW_FULL)
# Any backticked first cell at all, so a row with a non-canonical name (e.g.
# `Ghost-Skill`) is reported instead of being invisible to both lints.
TABLE_ROW_ANY_RE = re.compile(r"^\|\s*`([^`]+)`")
CANONICAL_NAME_RE = re.compile(r"[a-z0-9-]+")
# Markdown table separator row: `|---|:---:|`, `|:-|` etc. (GFM: one or more dashes).
TABLE_SEPARATOR_RE = re.compile(r"^\|\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
# Marketplace skill paths are relative and may target the explicit localized
# adapter root. Used with fullmatch: `$` would admit a trailing newline.
MANIFEST_SKILL_RE = re.compile(
    r"\./(?:(russian-academic-skills)/)?([a-z0-9-]+)"
)
# A count claim such as "4 skills" / "4 Skills" (word-bounded so "40 skillsets"
# is not one; case-insensitive because these are prose surfaces).
COUNT_CLAIM_RE = re.compile(r"\b(\d+) skills\b", re.IGNORECASE)


def _skill_locations(root: Path, violations: list[str]) -> dict[str, Path]:
    locations: dict[str, Path] = {}
    roots = (root,) + tuple(root / rel for rel in LOCALIZED_SKILL_ROOTS)
    for skill_root in roots:
        if not skill_root.is_dir():
            continue
        for skill_file in iter_skill_files(skill_root):
            name = skill_file.parent.name
            if name in locations:
                violations.append(
                    f"duplicate canonical skill name '{name}': "
                    f"{locations[name]} and {skill_file.parent}"
                )
                continue
            locations[name] = skill_file.parent
    return locations


def _skills_dir_entries(
    root: Path, locations: dict[str, Path], violations: list[str]
) -> set[str]:
    skills_dir = root / SKILLS_DIR
    if not skills_dir.is_dir():
        violations.append(f"{skills_dir}: directory is missing")
        return set()
    names: set[str] = set()
    for entry in sorted(skills_dir.iterdir(), key=lambda p: p.name):
        names.add(entry.name)
        expected = locations.get(entry.name, root / entry.name)
        if not entry.is_symlink():
            violations.append(
                f"{entry}: must be a symlink to ../{entry.name}, "
                f"found a real {'directory' if entry.is_dir() else 'file'}"
            )
            continue
        try:
            target = entry.resolve(strict=True)
        except (FileNotFoundError, RuntimeError):
            violations.append(f"{entry}: dangling symlink")
            continue
        if target != expected.resolve():
            violations.append(
                f"{entry}: symlink resolves to {target}, expected {expected}"
            )
    return names


def _overview_table_lines(section: str) -> list[str]:
    """The ONE table that immediately follows the heading: skip leading blank
    lines, then take the contiguous run of `|`-prefixed lines. A later table,
    prose mention, or fenced Markdown sample in the same section is not the
    inventory and must not satisfy the parity check."""
    lines = iter(section.splitlines())
    table: list[str] = []
    for line in lines:
        if line.strip() == "":
            if table:
                break
            continue
        if not line.lstrip().startswith("|"):
            break
        table.append(line)
    return table


def _cell_count(row: str) -> int:
    """Cells in a GFM table row: strip one leading and one trailing pipe,
    then split on unescaped pipes."""
    inner = row.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") else inner
    return len(re.split(r"(?<!\\)\|", inner))


def _claude_table_rows(root: Path, violations: list[str]) -> set[str]:
    claude_md = root / CLAUDE_MD
    if not claude_md.is_file():
        violations.append(f"{claude_md}: file is missing")
        return set()
    text = claude_md.read_text(encoding="utf-8")
    # Exact H2 line at column 0, outside code fences (shared helper): a
    # demoted `### Skills Overview` or a copy inside a fenced example is not
    # the section.
    section = heading_section(text, SKILLS_OVERVIEW_HEADING)
    if section is None:
        violations.append(
            f"{claude_md}: '{SKILLS_OVERVIEW_HEADING}' H2 is missing"
        )
        return set()
    rows: set[str] = set()
    table = _overview_table_lines(section)
    # A GFM table is header row + separator row + data rows. Both leading
    # rows are required (a table without its separator is not a table, and
    # the version lint would still read its rows). Every data row must carry
    # a backticked skill name in its first cell; one that does not (e.g.
    # `| ghost-skill v1.0.0 |`) is reported rather than dropped.
    if len(table) < 2 or not TABLE_SEPARATOR_RE.match(table[1]):
        violations.append(
            f"{claude_md}: '{SKILLS_OVERVIEW_HEADING}' is not followed by a GFM "
            f"table (header row then a |---| separator row)"
        )
        return set()
    header_cells, separator_cells = _cell_count(table[0]), _cell_count(table[1])
    if header_cells != separator_cells:
        # GFM: header and delimiter rows must have the same cell count or
        # GitHub does not render a table at all. Data-row width is NOT
        # checked: GFM pads/truncates data rows, and this lint reads only
        # the first cell, as check_version_consistency.py does.
        violations.append(
            f"{claude_md}: Skills Overview header has {header_cells} cells but "
            f"its separator row has {separator_cells}; GFM requires them equal"
        )
        return set()
    data_rows = table[2:]
    for line in data_rows:
        any_row = TABLE_ROW_ANY_RE.match(line)
        if any_row is None:
            violations.append(
                f"{claude_md}: Skills Overview data row {line.strip()!r} has no "
                f"backticked skill name in its first cell"
            )
            continue
        name = any_row.group(1)
        if CANONICAL_NAME_RE.fullmatch(name) is None:
            violations.append(
                f"{claude_md}: Skills Overview row names {name!r}, which is not "
                f"a canonical skill directory name ([a-z0-9-]+); both lints "
                f"would otherwise ignore this row"
            )
            continue
        rows.add(name)
        if TABLE_ROW_FULL_RE.match(line) is None:
            violations.append(
                f"{claude_md}: Skills Overview row for '{name}' lacks a "
                f"'vX.Y.Z' token after the name (check_version_consistency.py "
                f"skips such rows, so the version would go unchecked)"
            )
    if not rows:
        violations.append(
            f"{claude_md}: '{SKILLS_OVERVIEW_HEADING}' table has no "
            f"backticked skill rows"
        )
    return rows


def _load_json(path: Path, violations: list[str]) -> dict | None:
    if not path.is_file():
        violations.append(f"{path}: file is missing")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON ({exc.msg} at line {exc.lineno})")
        return None
    if not isinstance(data, dict):
        violations.append(f"{path}: top level must be an object")
        return None
    return data


def _marketplace_skills(
    root: Path, locations: dict[str, Path], violations: list[str]
) -> tuple[set[str], list[str]]:
    """Return (skill names across all plugins, plugin descriptions)."""
    path = root / MARKETPLACE_JSON
    data = _load_json(path, violations)
    if data is None:
        return set(), []
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        violations.append(f"{path}: 'plugins' must be a non-empty list")
        return set(), []
    names: set[str] = set()
    descriptions: list[str] = []
    if isinstance(data.get("description"), str):
        descriptions.append(data["description"])  # marketplace-level claim
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            violations.append(f"{path}: plugins[{index}] must be an object")
            continue
        description = plugin.get("description")
        if isinstance(description, str):
            descriptions.append(description)
        skills = plugin.get("skills")
        if not isinstance(skills, list):
            violations.append(
                f"{path}: plugins[{index}].skills must be a list of canonical relative "
                f"paths (symlink-blind importers read this list)"
            )
            continue
        for raw in skills:
            match = MANIFEST_SKILL_RE.fullmatch(raw) if isinstance(raw, str) else None
            if match is None:
                violations.append(
                    f"{path}: plugins[{index}].skills entry {raw!r} must be "
                    f"'./<name>' or './russian-academic-skills/<name>'"
                )
                continue
            name = match.group(2)
            names.add(name)
            expected = locations.get(name)
            manifest_target = root / raw[2:]
            if expected is not None and manifest_target.resolve() != expected.resolve():
                violations.append(
                    f"{path}: plugins[{index}].skills entry {raw!r} resolves to "
                    f"{manifest_target}, expected canonical directory {expected}"
                )
    return names, descriptions


def _check_count_claim(
    label: str, text: str, expected: int, violations: list[str]
) -> None:
    for claimed in COUNT_CLAIM_RE.findall(text):
        if int(claimed) != expected:
            violations.append(
                f"{label}: claims '{claimed} skills' but {expected} "
                f"relevant skill entries exist"
            )


def _report_set_diff(
    on_disk: set[str], other: set[str], surface: str, violations: list[str]
) -> None:
    for name in sorted(on_disk - other):
        violations.append(
            f"skill '{name}' exists on disk but "
            f"is not listed in {surface}"
        )
    for name in sorted(other - on_disk):
        violations.append(
            f"{surface} lists skill '{name}' but no canonical {name}/SKILL.md "
            f"exists"
        )


def run_all_checks(root: Path) -> list[str]:
    violations: list[str] = []
    locations = _skill_locations(root, violations)
    on_disk = set(locations)
    if not on_disk:
        violations.append(
            f"{root}: no canonical <name>/SKILL.md found (wrong --path?)"
        )
        return violations

    symlinked = _skills_dir_entries(root, locations, violations)
    _report_set_diff(on_disk, symlinked, f"{SKILLS_DIR}/ symlinks", violations)

    table = _claude_table_rows(root, violations)
    localized = {
        name
        for name, location in locations.items()
        if location.parent == root / LOCALIZED_SKILL_ROOTS[0]
    }
    _report_set_diff(
        on_disk - localized,
        table,
        f"{CLAUDE_MD} Skills Overview table",
        violations,
    )

    manifest, market_descriptions = _marketplace_skills(root, locations, violations)
    _report_set_diff(
        on_disk, manifest, f"{MARKETPLACE_JSON} plugins[].skills", violations
    )
    for description in market_descriptions:
        _check_count_claim(
            f"{MARKETPLACE_JSON} description", description, len(on_disk), violations
        )

    plugin = _load_json(root / PLUGIN_JSON, violations)
    if plugin is not None:
        description = plugin.get("description")
        if isinstance(description, str):
            _check_count_claim(
                f"{PLUGIN_JSON} description", description, len(on_disk), violations
            )

    registry = root / MODE_REGISTRY_MD
    if registry.is_file():
        _check_count_claim(
            str(MODE_REGISTRY_MD),
            registry.read_text(encoding="utf-8"),
            len(on_disk - localized),
            violations,
        )
    else:
        violations.append(f"{registry}: file is missing")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    args = parser.parse_args()
    violations = run_all_checks(args.path)
    if violations:
        for v in violations:
            print(f"ERROR: {v}")
        print(f"\n{len(violations)} violation(s) found.", file=sys.stderr)
        return 1
    print(
        "OK: skill inventory is identical across canonical directories, "
        "skills/ symlinks, the CLAUDE.md table, and the marketplace manifest."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
