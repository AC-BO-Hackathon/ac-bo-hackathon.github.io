#!/usr/bin/env python3
"""Suggest potential reviewers for the manuscript using Edison Scientific.

This script uses the official ``edison-client`` API
(https://docs.edisonscientific.com/) to run two jobs against the manuscript in
this repository:

1. An ``ANALYSIS`` (Finch) task with the manuscript **attached as an uploaded
   file**, asking the agent to propose potential peer reviewers (with
   affiliations, expertise, representative papers, and possible conflicts of
   interest to avoid).
2. A high-effort ``LITERATURE_HIGH`` (PaperQA) query on the manuscript's topic
   to surface closely related work and prominent authors who would make strong
   reviewer candidates.

Both tasks are submitted first and then polled concurrently, so they run at the
same time.

Usage
-----
    export EDISON_API_KEY=...           # your Edison Scientific API key
                                        # (EDISON_PLATFORM_API_KEY also accepted)
    pip install edison-client
    python scripts/edison_suggest_reviewers.py

Common options::

    # Attach a different manuscript file (or a directory of LaTeX sources)
    python scripts/edison_suggest_reviewers.py --manuscript copilot-main-fixed.pdf

    # Only run one of the two jobs
    python scripts/edison_suggest_reviewers.py --no-literature
    python scripts/edison_suggest_reviewers.py --no-analysis

Results (the formatted answers, and the analysis notebook when present) are
written to the ``--output-dir`` directory (default ``edison_output/``), along
with the Edison task IDs so the jobs can be fetched again later.

Notes
-----
* Per the official file-management docs, a *directory* must be uploaded as a
  single zipped collection (``as_collection=True``); uploading individual files
  separately can cause an ANALYSIS task to fail silently. This script uploads a
  directory as a collection automatically.
* To continue/refine a previous job, pass its task id via ``--continued-job-id``;
  it is attached to both tasks' ``RuntimeConfig``.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from uuid import UUID

REPO_ROOT = Path(__file__).resolve().parent.parent

# Manuscript candidates tried in order when --manuscript is not given.
DEFAULT_MANUSCRIPT_CANDIDATES = (
    "main.pdf",
    "copilot-main-fixed.pdf",
    "main.tex",
)

# The manuscript title/abstract are used to craft sensible default queries.
MANUSCRIPT_TITLE = "Bayesian Optimization Hackathon for Chemistry and Materials"

ANALYSIS_QUERY = (
    "The attached file is a manuscript titled "
    f"'{MANUSCRIPT_TITLE}', describing a community hackathon on Bayesian "
    "optimization for chemistry and materials science (Acceleration Consortium "
    "and Merck KGaA). Read the manuscript carefully and propose a ranked list "
    "of 10-15 potential peer reviewers suitable for a journal such as Digital "
    "Discovery (RSC). For each candidate provide: full name, current "
    "affiliation, a public email or profile URL if known, their specific area "
    "of expertise relevant to this manuscript, and 1-3 representative recent "
    "publications. Prioritize researchers active in Bayesian optimization, "
    "active learning, self-driving labs, and machine learning for materials and "
    "chemistry. Explicitly flag and EXCLUDE likely conflicts of interest "
    "(manuscript co-authors, very close collaborators, and same-institution "
    "candidates). Present the result as a clear table followed by short "
    "justifications."
)

LITERATURE_QUERY = (
    "Conduct a thorough, high-effort literature review on Bayesian optimization "
    "(and adjacent active-learning / self-driving-laboratory methods) for "
    "chemistry and materials science, with emphasis on community benchmarks, "
    "open-source software, and educational efforts in this area (e.g. work "
    "connected to the Acceleration Consortium). Identify the most closely "
    "related papers and the prominent, currently-active authors in this field "
    "who would be well qualified to peer review a manuscript titled "
    f"'{MANUSCRIPT_TITLE}'. For each key author, note their affiliation and a "
    "couple of representative papers. Provide full citations for all sources."
)

POLL_INTERVAL_SECONDS = 20


def find_manuscript(explicit: str | None) -> Path:
    """Return the manuscript path, validating that it exists."""
    if explicit:
        path = Path(explicit)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise FileNotFoundError(f"Manuscript not found: {path}")
        return path

    for candidate in DEFAULT_MANUSCRIPT_CANDIDATES:
        path = REPO_ROOT / candidate
        if path.exists():
            return path

    raise FileNotFoundError(
        "No manuscript found. Tried: "
        + ", ".join(DEFAULT_MANUSCRIPT_CANDIDATES)
        + ". Pass one explicitly with --manuscript."
    )


def build_runtime_config(continued_job_id: str | None):
    """Return a RuntimeConfig if any optional settings are needed, else None."""
    from edison_client.models.app import RuntimeConfig

    if continued_job_id:
        return RuntimeConfig(continued_job_id=UUID(continued_job_id))
    return None


def submit_tasks(client, manuscript: Path, *, run_analysis: bool,
                 run_literature: bool, continued_job_id: str | None):
    """Upload the manuscript and create the requested tasks.

    Returns a dict mapping a human label -> trajectory (task) id.
    """
    from edison_client import JobNames, TaskRequest

    task_ids: dict[str, str] = {}

    if run_analysis:
        # A directory must be uploaded as a single zipped collection; a single
        # file is uploaded as-is. ``upload_file`` returns a ``data_entry:<uuid>``
        # URI ready to attach to a task.
        if manuscript.is_dir():
            response = client.store_file_content(
                name=manuscript.name,
                file_path=manuscript,
                as_collection=True,
                description="Manuscript source bundle for reviewer suggestion.",
            )
            file_uri = f"data_entry:{response.data_storage.id}"
        else:
            file_uri = client.upload_file(
                file_path=manuscript,
                description="Manuscript for reviewer suggestion.",
            )
        print(f"Uploaded manuscript '{manuscript.name}' -> {file_uri}")

        analysis_task = TaskRequest(
            name=JobNames.ANALYSIS,
            query=ANALYSIS_QUERY,
            runtime_config=build_runtime_config(continued_job_id),
        )
        analysis_id = client.create_task(analysis_task, files=[file_uri])
        task_ids["analysis"] = str(analysis_id)
        print(f"Submitted ANALYSIS task: {analysis_id}")

    if run_literature:
        literature_task = TaskRequest(
            name=JobNames.LITERATURE_HIGH,
            query=LITERATURE_QUERY,
            runtime_config=build_runtime_config(continued_job_id),
        )
        literature_id = client.create_task(literature_task)
        task_ids["literature"] = str(literature_id)
        print(f"Submitted LITERATURE_HIGH task: {literature_id}")

    return task_ids


def poll_until_done(client, task_ids: dict[str, str], timeout: float):
    """Poll all tasks concurrently until every one reaches a terminal state."""
    from edison_client.models.rest import ExecutionStatus

    pending = dict(task_ids)
    completed: dict[str, object] = {}
    start = time.monotonic()

    while pending:
        if timeout and timeout > 0 and (time.monotonic() - start) > timeout:
            print(
                f"Timed out after {timeout}s with {len(completed)}/"
                f"{len(task_ids)} tasks complete.",
                file=sys.stderr,
            )
            break

        for label, task_id in list(pending.items()):
            status = client.get_task(task_id=task_id, lite=True)
            if ExecutionStatus(status.status).is_terminal_state():
                full = client.get_task(task_id=task_id, lite=False)
                completed[label] = full
                del pending[label]
                print(f"[{label}] finished with status: {status.status}")
            else:
                print(f"[{label}] status: {status.status}")

        if pending:
            time.sleep(POLL_INTERVAL_SECONDS)

    return completed


def save_result(label: str, result, output_dir: Path) -> None:
    """Persist a task's answer (and notebook, when present) to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    answer = (
        getattr(result, "formatted_answer", None)
        or getattr(result, "answer", None)
        or ""
    )
    answer_path = output_dir / f"{label}_answer.md"
    answer_path.write_text(answer, encoding="utf-8")
    print(f"[{label}] wrote answer -> {answer_path} ({len(answer)} chars)")

    notebook = getattr(result, "notebook", None)
    if notebook:
        notebook_path = output_dir / f"{label}_notebook.ipynb"
        notebook_path.write_text(
            notebook if isinstance(notebook, str) else json.dumps(notebook),
            encoding="utf-8",
        )
        print(f"[{label}] wrote notebook -> {notebook_path}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manuscript",
        help="Path to the manuscript file or LaTeX source directory to attach.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "edison_output"),
        help="Directory to write results to (default: edison_output/).",
    )
    parser.add_argument(
        "--continued-job-id",
        help="UUID of a previous Edison task to continue/refine.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=3600.0,
        help="Maximum seconds to wait for tasks to finish (default: 3600; "
             "use 0 or a negative value to wait indefinitely).",
    )
    parser.add_argument(
        "--no-analysis",
        dest="run_analysis",
        action="store_false",
        help="Skip the manuscript ANALYSIS reviewer-suggestion task.",
    )
    parser.add_argument(
        "--no-literature",
        dest="run_literature",
        action="store_false",
        help="Skip the high-effort LITERATURE_HIGH query.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    import os

    args = parse_args(argv)

    if not args.run_analysis and not args.run_literature:
        print("Nothing to do: both tasks were disabled.", file=sys.stderr)
        return 2

    api_key = os.environ.get("EDISON_API_KEY") or os.environ.get(
        "EDISON_PLATFORM_API_KEY"
    )
    if not api_key:
        print(
            "No Edison API key found. Export EDISON_API_KEY (or "
            "EDISON_PLATFORM_API_KEY) before running:\n"
            "    export EDISON_API_KEY=...",
            file=sys.stderr,
        )
        return 1

    try:
        from edison_client import EdisonClient
    except ImportError:
        print(
            "edison-client is not installed. Install it with:\n"
            "    pip install edison-client",
            file=sys.stderr,
        )
        return 1

    manuscript = find_manuscript(args.manuscript) if args.run_analysis else None
    output_dir = Path(args.output_dir)

    client = EdisonClient(api_key=api_key)

    task_ids = submit_tasks(
        client,
        manuscript,
        run_analysis=args.run_analysis,
        run_literature=args.run_literature,
        continued_job_id=args.continued_job_id,
    )

    # Record task ids immediately so the jobs can be fetched again later even if
    # polling is interrupted.
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "task_ids.json").write_text(
        json.dumps(task_ids, indent=2), encoding="utf-8"
    )

    results = poll_until_done(client, task_ids, timeout=args.timeout)

    for label, result in results.items():
        save_result(label, result, output_dir)

    missing = set(task_ids) - set(results)
    if missing:
        print(
            "Some tasks did not finish in time: "
            + ", ".join(sorted(missing))
            + f". Re-fetch them later using the IDs in {output_dir / 'task_ids.json'}.",
            file=sys.stderr,
        )
        return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
