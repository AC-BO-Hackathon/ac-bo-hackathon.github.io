#!/usr/bin/env python3
"""Run Edison Scientific queries that support the Digital Discovery revision.

The referees asked the authors to add substantial *synthesis* to the AC-BO
Hackathon manuscript: (i) forward-looking opportunities for Bayesian
optimization (BO) in chemistry and materials, (ii) scientific lessons about
where BO helps and where it struggles, and (iii) a reflective meta-analysis of
the hackathon as a community-research/education model.  This script submits a
small set of high-effort literature/analysis jobs against the Edison Scientific
platform to gather citable evidence for those sections.

It intentionally mirrors ``scripts/edison_suggest_reviewers.py`` so the two
share the same, documented ``edison-client`` usage pattern.

Usage
-----
    export EDISON_PLATFORM_API_KEY=...      # (EDISON_API_KEY also accepted)
    pip install edison-client

    # Submit all jobs, record their task IDs, and return immediately:
    python scripts/edison_reviewer_feedback.py submit

    # Later (or in a follow-up session), poll + save any finished answers:
    python scripts/edison_reviewer_feedback.py fetch

Task IDs are written to ``edison_output/reviewer_feedback_task_ids.json`` so the
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
TASK_IDS_PATH = OUTPUT_DIR / "reviewer_feedback_task_ids.json"

POLL_INTERVAL_SECONDS = 30

MANUSCRIPT_TITLE = "Bayesian Optimization Hackathon for Chemistry and Materials"

# Attached to the ANALYSIS job when present (manuscript for grounding).
MANUSCRIPT_CANDIDATES = ("copilot-main-fixed.pdf", "main.pdf", "main.tex")

# ---------------------------------------------------------------------------
# Queries.  Each is written so the answer surfaces concrete, citable papers.
# ---------------------------------------------------------------------------

FUTURE_OPPORTUNITIES_QUERY = (
    "High-effort literature review of FUTURE OPPORTUNITIES for Bayesian "
    "optimization (BO) in chemistry and materials discovery. Cover each of the "
    "following directions as a separate short subsection and, for EACH, give "
    "one or two of the most relevant recent (ideally 2021-2025) papers with "
    "FULL citations (authors, title, venue, year, DOI): (1) BO for autonomous "
    "/ self-driving laboratories; (2) multi-fidelity BO; (3) uncertainty-aware "
    "experimental planning / active learning; (4) foundation-model- and "
    "large-language-model-assisted BO; (5) preference-based / human-in-the-loop "
    "BO; (6) multi-objective materials design; (7) robust BO under noisy "
    "experimental data; (8) community benchmark development for BO; and (9) "
    "domain-specific BO tools for synthesis and processing optimization. "
    "Prefer chemistry/materials applications. Provide a consolidated reference "
    "list with DOIs at the end."
)

SCIENTIFIC_LESSONS_QUERY = (
    "High-effort literature review of the demonstrated STRENGTHS and "
    "LIMITATIONS of Bayesian optimization (BO) in chemistry and materials "
    "science, suitable for a discussion of scientific lessons learned. "
    "Strengths to substantiate with citations: performance in low-data / "
    "data-scarce regimes, multi-objective search, transfer learning and "
    "warm-starting, molecular and materials screening, and human-in-the-loop "
    "workflows. Limitations to substantiate with citations: sensitivity to "
    "molecular representation and featurization, kernel choice, quality of "
    "warm-start data, noisy observations, high-dimensional search spaces, "
    "batch-size selection, acquisition-function optimization, computational "
    "overhead, and reproducibility of benchmark comparisons. Also address "
    "whether particular BO frameworks are agreed to work better for noisy "
    "versus low-noise data, and how readily BO tools deploy in real "
    "experimental settings. Provide FULL citations with DOIs."
)

HACKATHON_IMPACT_QUERY = (
    "High-effort literature review on scientific hackathons and community "
    "coding events as a model for research training and open-source output in "
    "computational science, chemistry, materials, and machine learning. Find "
    "evidence and full citations (with DOIs) for: measurable outcomes and "
    "'lessons learned' from organizing such hackathons; whether participants "
    "subsequently adopt the methods in their own research (follow-up impact); "
    "how prior participant expertise relates to outcomes; and best practices "
    "for judging, mentoring, team formation, and post-event archiving. Include "
    "prior chemistry/materials and large-language-model hackathon reports. "
    "Provide a consolidated reference list with DOIs."
)

CLASSIFICATION_ANALYSIS_QUERY = (
    "The attached PDF is the manuscript '" + MANUSCRIPT_TITLE + "', which "
    "summarizes 45 projects from a 2-day virtual Bayesian-optimization (BO) "
    "hackathon for chemistry and materials. Using the project descriptions in "
    "the manuscript, perform a META-ANALYSIS across the projects: (a) classify "
    "each project into one of these output categories -- mature software, "
    "benchmark dataset/problem, tutorial/educational, application "
    "demonstration, or preliminary concept -- and give the category counts; "
    "(b) identify the dominant application domains and which BO software "
    "frameworks (e.g., BoTorch, Ax, BayBE, GAUCHE, Gryffin/Atlas, scikit-optimize) "
    "recur across teams; (c) note common methodological choices and "
    "differences in how teams approached their problems; (d) highlight how many "
    "projects explored large language models (LLMs) or generative models; and "
    "(e) summarize the main strengths and limitations of BO that the projects "
    "collectively reveal. Emphasize that the hackathon spanned only two days, "
    "so conclusions are necessarily preliminary and should not be "
    "over-interpreted. Present category counts as a table."
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


def _find_manuscript() -> Path | None:
    for candidate in MANUSCRIPT_CANDIDATES:
        path = REPO_ROOT / candidate
        if path.exists():
            return path
    return None


def submit(argv: argparse.Namespace) -> int:
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=_api_key())
    task_ids: dict[str, str] = {}

    literature_jobs = {
        "future_opportunities": FUTURE_OPPORTUNITIES_QUERY,
        "scientific_lessons": SCIENTIFIC_LESSONS_QUERY,
        "hackathon_impact": HACKATHON_IMPACT_QUERY,
    }
    for label, query in literature_jobs.items():
        task = TaskRequest(name=JobNames.LITERATURE_HIGH, query=query)
        task_id = client.create_task(task)
        task_ids[label] = str(task_id)
        print(f"Submitted LITERATURE_HIGH [{label}]: {task_id}")

    if not argv.no_analysis:
        manuscript = _find_manuscript()
        if manuscript is not None:
            file_uri = client.upload_file(
                file_path=manuscript,
                description="AC-BO hackathon manuscript for meta-analysis.",
            )
            print(f"Uploaded manuscript '{manuscript.name}' -> {file_uri}")
            task = TaskRequest(
                name=JobNames.ANALYSIS, query=CLASSIFICATION_ANALYSIS_QUERY
            )
            task_id = client.create_task(task, files=[file_uri])
            task_ids["classification_analysis"] = str(task_id)
            print(f"Submitted ANALYSIS [classification_analysis]: {task_id}")
        else:
            print("No manuscript file found; skipping ANALYSIS task.")

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

    notebook = getattr(result, "notebook", None)
    if notebook:
        nb = OUTPUT_DIR / f"{label}_notebook.ipynb"
        nb.write_text(
            notebook if isinstance(notebook, str) else json.dumps(notebook),
            encoding="utf-8",
        )
        print(f"[{label}] wrote notebook -> {nb}")


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
                print(f"[{label}] status: {status.status}")
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
    p_submit.add_argument(
        "--no-analysis", action="store_true", help="Skip the ANALYSIS job."
    )
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
