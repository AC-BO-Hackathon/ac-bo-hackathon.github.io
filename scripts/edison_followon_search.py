#!/usr/bin/env python3
"""Search for published or otherwise follow-on work connected to the AC-BO Hackathon.

Companion to ``edison_suggest_reviewers.py``. Submits Edison Scientific
``LITERATURE_HIGH`` (PaperQA) tasks that look for papers, preprints, software
releases and datasets that arose from -- or explicitly acknowledge -- the
Acceleration Consortium Bayesian Optimization Hackathon (online, 4-5 March
2024), and polls them to completion.

Usage
-----
    export EDISON_PLATFORM_API_KEY=...
    pip install edison-client
    python scripts/edison_followon_search.py            # submit + wait
    python scripts/edison_followon_search.py --wait-only  # resume from task_ids.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / "edison_output" / "followon"
POLL_INTERVAL_SECONDS = 60

EVENT = (
    "the Acceleration Consortium Bayesian Optimization Hackathon for Chemistry "
    "and Materials (the 'AC BO Hackathon 2024'), a two-day online event held "
    "4-5 March 2024, organized by the Acceleration Consortium (University of "
    "Toronto) with Merck KGaA, which produced 45 team projects archived on "
    "GitHub (github.com/AC-BO-Hackathon) and Zenodo"
)

QUERIES = {
    # 1. Direct descendants: anything citing/acknowledging the event itself.
    "event_descendants": (
        f"Find every published paper, preprint (arXiv, ChemRxiv, bioRxiv), "
        f"software release, dataset or benchmark that arose from, acknowledges, "
        f"or explicitly cites {EVENT}. Include works that mention the hackathon "
        "in their acknowledgements, that describe a project first prototyped at "
        "the hackathon, or that cite the hackathon website, its Zenodo "
        "archives, or the hackathon manuscript. For each hit give: full "
        "citation with DOI/arXiv ID, publication date, authors, and one "
        "sentence on exactly how it connects to the hackathon and how strong "
        "that connection is. Distinguish (a) works that name the hackathon "
        "explicitly from (b) works by hackathon participants on the same topic "
        "with no explicit link. Say plainly if a category is empty rather than "
        "padding the answer with loosely related Bayesian optimization papers."
    ),
    # 2. Project-by-project: did any of the 45 project topics become a paper?
    "project_followups": (
        "Below is the list of the 45 team projects from "
        f"{EVENT}. For each, determine whether the same team (or its members) "
        "subsequently published a paper, preprint, or a maintained software "
        "package on that same topic AFTER March 2024. Report only concrete "
        "matches with full citations (DOI or arXiv ID) and publication dates, "
        "and state explicitly which projects have no traceable follow-up. "
        "Projects:\n" + "PROJECT_LIST_PLACEHOLDER"
    ),
    # 3. Downstream use of the specific artifacts the hackathon released.
    "artifact_uptake": (
        "Determine whether the following research artifacts, all first released "
        f"at or immediately after {EVENT}, have since been used, cited, "
        "benchmarked against, or extended in the peer-reviewed or preprint "
        "literature: (a) ScattBO, a benchmark for Bayesian optimisation of "
        "materials discovery from scattering data (Andy S. Anker); (b) the "
        "GAUCHE library tutorial for Gaussian processes in chemistry (Ryan-Rhys "
        "Griffiths, Leo Klarner); (c) RAMBO, retrieval-augmented initialization "
        "for Bayesian optimization of chemical reactions (Schwaller group, "
        "EPFL); (d) BayBE, the Bayesian Back End from Merck KGaA (Martin "
        "Fitzner, Adrian Sosic, Alexander Hopp); (e) MolDAIS for molecular "
        "descriptor selection (Ohio State, Farshud Sorourifar, Joel Paulson); "
        "(f) Honegumi, a template generator for Bayesian optimization scripts "
        "(Sterling G. Baird); (g) the 'awesome Bayesian optimization' list "
        "(Materials Data Facility, Ben Blaiszik). For each, list the citing or "
        "extending works with full citations and dates, and state which have no "
        "documented uptake."
    ),
}


def build_project_list() -> str:
    import re

    lines = []
    for path in sorted((REPO_ROOT / "_projects").glob("project-*.md")):
        text = path.read_text(encoding="utf-8")
        front = text.split("---")[1] if text.startswith("---") else ""

        def field(key: str) -> str:
            m = re.search(rf"^{key}:\s*(.+)$", front, re.M)
            return m.group(1).strip() if m else ""

        num = field("number").split("#")[0].split("<!--")[0].strip()
        title = field("title")
        repo = field("github")
        leads = re.findall(r"^\s+-\s+(.+)$", front, re.M)
        lead = re.sub(r"<[^>]+>|\(|\)|@\S+", "", leads[0]).strip() if leads else ""
        if title and not title.startswith("topic:"):
            lines.append(
                f"{num}. {title}" + (f" -- lead: {lead}" if lead else "")
                + (f" -- repo: github.com/{repo}" if repo else "")
            )
    return "\n".join(lines)


def submit(client, labels):
    from edison_client import JobNames, TaskRequest

    project_list = build_project_list()
    ids = {}
    for label in labels:
        query = QUERIES[label].replace("PROJECT_LIST_PLACEHOLDER", project_list)
        task_id = client.create_task(
            TaskRequest(name=JobNames.LITERATURE_HIGH, query=query)
        )
        ids[label] = str(task_id)
        print(f"Submitted {label}: {task_id}", flush=True)
    return ids


def poll(client, ids: dict, timeout: float, output_dir: Path):
    from edison_client.models.rest import ExecutionStatus

    pending = dict(ids)
    start = time.monotonic()
    while pending:
        if timeout > 0 and (time.monotonic() - start) > timeout:
            print(f"Timed out; still pending: {sorted(pending)}", file=sys.stderr)
            break
        for label, task_id in list(pending.items()):
            status = client.get_task(task_id=task_id, lite=True)
            if ExecutionStatus(status.status).is_terminal_state():
                full = client.get_task(task_id=task_id, lite=False)
                save(label, full, output_dir)
                del pending[label]
                print(f"[{label}] terminal: {status.status}", flush=True)
            else:
                print(f"[{label}] {status.status}", flush=True)
        if pending:
            time.sleep(POLL_INTERVAL_SECONDS)
    return sorted(pending)


def save(label: str, result, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    answer = (
        getattr(result, "formatted_answer", None)
        or getattr(result, "answer", None)
        or ""
    )
    (output_dir / f"{label}_answer.md").write_text(answer, encoding="utf-8")
    print(f"[{label}] wrote {len(answer)} chars", flush=True)
    notebook = getattr(result, "notebook", None)
    if notebook:
        (output_dir / f"{label}_notebook.ipynb").write_text(
            notebook if isinstance(notebook, str) else json.dumps(notebook),
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--timeout", type=float, default=3000.0)
    parser.add_argument("--wait-only", action="store_true",
                        help="Skip submission; poll the IDs in task_ids.json.")
    parser.add_argument("--labels", nargs="*", default=list(QUERIES))
    args = parser.parse_args()

    api_key = os.environ.get("EDISON_PLATFORM_API_KEY") or os.environ.get(
        "EDISON_API_KEY"
    )
    if not api_key:
        print("No Edison API key in the environment.", file=sys.stderr)
        return 1

    from edison_client import EdisonClient

    client = EdisonClient(api_key=api_key)
    output_dir = Path(args.output_dir)
    ids_path = output_dir / "task_ids.json"

    if args.wait_only:
        ids = json.loads(ids_path.read_text())
    else:
        ids = submit(client, args.labels)
        output_dir.mkdir(parents=True, exist_ok=True)
        ids_path.write_text(json.dumps(ids, indent=2), encoding="utf-8")

    unfinished = poll(client, ids, args.timeout, output_dir)
    return 1 if unfinished else 0


if __name__ == "__main__":
    raise SystemExit(main())
