#!/usr/bin/env python3
"""Validate a newly created article file and the changelog before PR creation.

Usage:
    python validate_article.py <path-to-article.md>

Exits non-zero on any validation error.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CHANGELOG = REPO_ROOT / "docs" / "_data" / "changelog.yml"

REQUIRED_FIELDS = {"layout", "title", "author", "category", "tags", "date"}
BAD_FILENAME_CHARS = set("?#&%+")


def validate_frontmatter(path: Path) -> list[str]:
    """Check that the article has valid YAML frontmatter with all required fields."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        errors.append("No YAML frontmatter found (missing --- delimiters).")
        return errors

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"YAML parse error in frontmatter: {exc}")
        return errors

    if not isinstance(fm, dict):
        errors.append("Frontmatter is not a YAML mapping.")
        return errors

    # Check required fields
    missing = REQUIRED_FIELDS - set(fm.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(sorted(missing))}")

    # Check fixed values
    if fm.get("layout") != "post":
        errors.append(f'layout must be "post", got "{fm.get("layout")}".')
    if fm.get("tags") != "分类":
        errors.append(f'tags must be "分类", got "{fm.get("tags")}".')

    # Check date format (the date field string before the time part)
    date_val = str(fm.get("date", ""))
    date_str = date_val.split()[0] if date_val else ""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        errors.append(f"Date does not match YYYY-MM-DD pattern: {date_str}")

    return errors


def validate_filename(path: Path) -> list[str]:
    """Check filename for URL-breaking characters."""
    errors: list[str] = []
    bad = BAD_FILENAME_CHARS & set(path.name)
    if bad:
        errors.append(
            f"Filename contains URL-breaking characters: {', '.join(sorted(bad))} "
            f"in '{path.name}'"
        )
    return errors


def validate_changelog() -> list[str]:
    """Check that changelog.yml is valid YAML with the expected structure."""
    errors: list[str] = []
    if not CHANGELOG.exists():
        errors.append(f"Changelog not found: {CHANGELOG}")
        return errors

    try:
        data = yaml.safe_load(CHANGELOG.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"Changelog YAML parse error: {exc}")
        return errors

    if not isinstance(data, list):
        errors.append("Changelog root is not a list.")
        return errors

    if len(data) == 0:
        errors.append("Changelog is empty.")
        return errors

    first = data[0]
    if not isinstance(first, dict):
        errors.append("First changelog entry is not a mapping.")
        return errors

    for key in ("date", "commit_message", "changes"):
        if key not in first:
            errors.append(f"First changelog entry missing key: {key}")

    if "changes" in first:
        if not isinstance(first["changes"], list) or len(first["changes"]) == 0:
            errors.append("First changelog entry 'changes' must be a non-empty list.")
        else:
            for i, change in enumerate(first["changes"]):
                if not isinstance(change, dict):
                    errors.append(f"changes[{i}] is not a mapping.")
                elif "title" not in change or "url" not in change:
                    errors.append(f"changes[{i}] missing 'title' or 'url'.")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate_article.py <path-to-article.md>", file=sys.stderr)
        sys.exit(1)

    article_path = Path(sys.argv[1])
    if not article_path.exists():
        print(f"ERROR: Article file not found: {article_path}", file=sys.stderr)
        sys.exit(1)

    all_errors: list[str] = []

    print(f"Validating article: {article_path}")
    all_errors.extend(validate_frontmatter(article_path))
    all_errors.extend(validate_filename(article_path))

    print("Validating changelog...")
    all_errors.extend(validate_changelog())

    if all_errors:
        print("\nValidation FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("All validations passed.")


if __name__ == "__main__":
    main()
