#!/usr/bin/env python3
"""Analyze the code repositories associated with the hackathon projects.

Referee 1 asked for a more systematic evaluation of the project outputs,
including code availability and licensing across the repositories. This script
reads the project spreadsheet (``AC-bo-hackathon-2024.csv``), extracts the
unique GitHub repositories, and queries the GitHub REST API (via the ``gh``
CLI) for each repository's license, primary language, archive status, and last
push date. It writes a machine-readable summary to
``edison_output/repo_license_analysis.json`` and prints an aggregate license
distribution.

Usage
-----
    gh auth login              # or set GITHUB_TOKEN
    python scripts/analyze_project_repos.py

The committed JSON output records the result so the aggregate figures used in
the manuscript remain reproducible even without re-querying GitHub.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "AC-bo-hackathon-2024.csv"
OUTPUT_PATH = REPO_ROOT / "edison_output" / "repo_license_analysis.json"

REPO_RE = re.compile(r"github\.com/([^/\s]+/[^/\s#?]+)")


def unique_repos() -> dict[str, str]:
    """Return a mapping of ``owner/repo`` -> first project number seen."""
    repos: dict[str, str] = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw = (row.get("Github Repo") or "").strip()
            match = REPO_RE.search(raw)
            if not match:
                continue
            slug = match.group(1).rstrip("/")
            if slug.endswith(".git"):
                slug = slug[: -len(".git")]
            repos.setdefault(slug, row.get("Project num", ""))
    return repos


def query_repo(slug: str) -> dict:
    """Query a single repository via the ``gh`` CLI. Best-effort."""
    jq = (
        "{full_name:.full_name,"
        'license:(.license.spdx_id // "NONE"),'
        "archived:.archived,pushed_at:.pushed_at,"
        'language:(.language // null)}'
    )
    try:
        proc = subprocess.run(
            ["gh", "api", f"repos/{slug}", "--jq", jq],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        return {"queried": slug, "accessible": False, "error": str(exc)[:80]}
    if proc.returncode != 0:
        return {
            "queried": slug,
            "accessible": False,
            "error": proc.stderr.strip()[:80],
        }
    data = json.loads(proc.stdout)
    data.update({"queried": slug, "accessible": True})
    return data


def main() -> int:
    repos = unique_repos()
    results = [query_repo(slug) for slug in sorted(repos)]

    licenses: Counter[str] = Counter()
    for item in results:
        if item.get("accessible"):
            licenses[item.get("license", "NONE")] += 1
        else:
            licenses["INACCESSIBLE"] += 1

    payload = {
        "n_repo_links": len(results),
        "license_distribution": dict(licenses.most_common()),
        "repositories": results,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Unique repository links: {len(results)}")
    print("License distribution:")
    for name, count in licenses.most_common():
        print(f"  {name}: {count}")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
