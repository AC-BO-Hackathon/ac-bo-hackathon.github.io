#!/usr/bin/env python3
"""Run Edison Scientific queries about accessible interfaces for Bayesian optimization.

Issue #174 asks for a literature survey of GUIs and other accessible formats
(web apps, no-code platforms, template generators) for deploying Bayesian
optimization (BO) in experimental settings, to support the Digital Discovery
revision in PR #171 and the referee question about whether BO tools are easily
deployable by experimentalists.

It mirrors ``scripts/edison_suggest_reviewers.py`` and
``scripts/edison_reviewer_feedback.py`` so all three share the same documented
``edison-client`` usage pattern.

Usage
-----
    export EDISON_PLATFORM_API_KEY=...      # (EDISON_API_KEY also accepted)
    pip install edison-client

    # Submit all jobs, record their task IDs, and return immediately:
    python scripts/edison_bo_gui_tools.py submit

    # Later (or in a follow-up session), poll + save any finished answers:
    python scripts/edison_bo_gui_tools.py fetch --timeout 2400

Task IDs are written to ``edison_output/bo_gui_tools_task_ids.json`` so the
jobs can always be re-fetched, even across sessions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "edison_output"
TASK_IDS_PATH = OUTPUT_DIR / "bo_gui_tools_task_ids.json"

POLL_INTERVAL_SECONDS = 30

# ---------------------------------------------------------------------------
# Queries.  Each is written so the answer surfaces concrete, citable papers.
# ---------------------------------------------------------------------------

GUI_TOOLS_QUERY = (
    "High-effort literature review of software tools that make Bayesian "
    "optimization (BO) accessible to experimental scientists who are not "
    "expert programmers, published roughly 2020-2026. Cover graphical user "
    "interfaces (GUIs), web applications, no-code or low-code platforms, "
    "spreadsheet-style interfaces, interactive dashboards, and code-template "
    "or scaffold generators for BO-guided design of experiments in chemistry, "
    "materials science, and adjacent laboratory sciences. For EACH tool "
    "report: tool name; interface style (desktop GUI, web app, notebook "
    "widget, template generator, etc.); intended users; whether it targets "
    "experimental/wet-lab optimization campaigns; open-source status; and a "
    "FULL citation (authors, title, venue, year, DOI). Include tools "
    "published in the Journal of Open Source Software (JOSS), SoftwareX, "
    "Digital Discovery, npj Computational Materials, and similar venues. "
    "Examples of the category include Honegumi (an interactive template "
    "generator, npj Computational Materials) and Web-BO (a web GUI for "
    "chemistry, Digital Discovery); find as many ADDITIONAL published tools "
    "as possible beyond these, for example desktop or web GUIs such as "
    "BOXVIA, EDBO+, AutoOED, ProcessOptimizer and its Brownie Bee front end, "
    "NIMS-OS, and any others you can locate. Provide a consolidated "
    "reference list with DOIs at the end."
)

JOSS_GUI_QUERY = (
    "Identify peer-reviewed SOFTWARE papers, especially in the Journal of "
    "Open Source Software (JOSS) and also SoftwareX, Digital Discovery, "
    "Chemistry-Methods, npj Computational Materials, and Machine Learning: "
    "Science and Technology, that present graphical user interfaces, web "
    "applications, dashboards, or other low-barrier interfaces for Bayesian "
    "optimization or sequential/adaptive design of experiments aimed at "
    "experimentalists rather than programmers. For each paper give the tool "
    "name, a one-sentence description of the interface and its target "
    "audience, and a FULL citation (authors, title, venue, year, DOI). Also "
    "note any GUI front ends built on top of established BO libraries such "
    "as BoTorch/Ax, scikit-optimize, GPyOpt, Optuna, or BayBE, and whether "
    "each tool supports batch experiments, multi-objective optimization, and "
    "categorical/mixed variables. Provide a consolidated reference list with "
    "DOIs at the end."
)

DEPLOYABILITY_QUERY = (
    "High-effort literature review addressing the question: are Bayesian "
    "optimization (BO) tools easily deployable by experimentalists in real "
    "laboratory data settings? Gather citable evidence (roughly 2019-2026, "
    "full citations with DOIs) on: (1) documented cases where experimental "
    "chemists or materials scientists deployed BO in wet-lab optimization "
    "campaigns, and which software they used; (2) reported barriers to "
    "adoption, for example programming expertise, problem formulation and "
    "search-space specification, software installation, and integration with "
    "instruments and data infrastructure; (3) how accessible interfaces "
    "(GUIs, web apps, spreadsheet interfaces, and code-template generators "
    "such as Honegumi) plus tutorials and benchmarks lower those barriers; "
    "and (4) remaining gaps between BO software maturity and routine "
    "laboratory deployment. Provide a consolidated reference list with DOIs "
    "at the end."
)


def _api_key() -> str:
    key = os.environ.get("EDISON_API_KEY") or os.environ.get(
        "EDISON_PLATFORM_API_KEY"
    )
    if not key:
        print(
            "No Edison API key found. Export EDISON_API_KEY or "
            "EDISON_PLATFORM_API_KEY.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return key


def submit(argv: argparse.Namespace) -> int:
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=_api_key())
    task_ids: dict[str, str] = {}

    literature_jobs = {
        "bo_gui_tools": GUI_TOOLS_QUERY,
        "bo_joss_gui": JOSS_GUI_QUERY,
        "bo_deployability": DEPLOYABILITY_QUERY,
    }
    for label, query in literature_jobs.items():
        task = TaskRequest(name=JobNames.LITERATURE_HIGH, query=query)
        task_id = client.create_task(task)
        task_ids[label] = str(task_id)
        print(f"Submitted LITERATURE_HIGH [{label}]: {task_id}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TASK_IDS_PATH.write_text(json.dumps(task_ids, indent=2), encoding="utf-8")
    print(f"Recorded {len(task_ids)} task IDs -> {TASK_IDS_PATH}")
    return 0


def _save_result(label: str, result) -> None:
    answer = (
        getattr(result, "formatted_answer", None)
        or getattr(result, "answer", None)
        or ""
    )
    out = OUTPUT_DIR / f"{label}_answer.md"
    out.write_text(answer, encoding="utf-8")
    print(f"[{label}] wrote answer -> {out} ({len(answer)} chars)")


def fetch(argv: argparse.Namespace) -> int:
    from edison_client import EdisonClient
    from edison_client.models.rest import ExecutionStatus

    if not TASK_IDS_PATH.exists():
        print(f"No task IDs at {TASK_IDS_PATH}; run 'submit' first.", file=sys.stderr)
        return 1

    task_ids = json.loads(TASK_IDS_PATH.read_text(encoding="utf-8"))
    client = EdisonClient(api_key=_api_key())

    pending = dict(task_ids)
    start = time.monotonic()
    while pending:
        for label, task_id in list(pending.items()):
            status = client.get_task(task_id=task_id, lite=True)
            if ExecutionStatus(status.status).is_terminal_state():
                full = client.get_task(task_id=task_id, lite=False)
                _save_result(label, full)
                print(f"[{label}] finished: {status.status}")
                del pending[label]
            else:
                print(f"[{label}] status: {status.status}", flush=True)
        if not pending:
            break
        if argv.timeout and (time.monotonic() - start) > argv.timeout:
            print(
                f"Timed out with {len(pending)} task(s) still running: "
                + ", ".join(sorted(pending)),
                file=sys.stderr,
            )
            return 1
        time.sleep(POLL_INTERVAL_SECONDS)
    print("All tasks fetched.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_submit = sub.add_parser("submit", help="Submit all Edison jobs.")
    p_submit.set_defaults(func=submit)

    p_fetch = sub.add_parser("fetch", help="Poll and save finished answers.")
    p_fetch.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Max seconds to keep polling (0 = wait indefinitely).",
    )
    p_fetch.set_defaults(func=fetch)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
