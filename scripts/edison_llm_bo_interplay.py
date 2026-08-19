#!/usr/bin/env python3
"""Run Edison Scientific queries on the interplay between LLMs and BO.

Issue #173 asks for manuscripts and repositories, from before and especially
since the AC-BO Hackathon (spring 2024), on how large language models (LLMs)
and Bayesian optimization (BO) are used, separately or together, for materials
discovery and related tasks. The answers feed the "foundation-model- and
LLM-assisted BO" discussion in the Future Opportunities section that PR #171
adds to the Digital Discovery manuscript. One query focuses on the Cooper
group's recent work (BORA, IJCAI 2025; and the closed-loop scientific
reasoning study in Digital Discovery, 2026, which pairs a petanque simulation
with chemistry problems and analyzes LLM reasoning chains).

It intentionally mirrors ``scripts/edison_suggest_reviewers.py`` and
``scripts/edison_reviewer_feedback.py`` so all three share the same,
documented ``edison-client`` usage pattern.

Usage
-----
    export EDISON_PLATFORM_API_KEY=...      # (EDISON_API_KEY also accepted)
    pip install edison-client

    # Submit all jobs, record their task IDs, and return immediately:
    python scripts/edison_llm_bo_interplay.py submit

    # Later (or in a follow-up session), poll + save any finished answers:
    python scripts/edison_llm_bo_interplay.py fetch

Task IDs are written to ``edison_output/llm_bo_interplay_task_ids.json`` so
the jobs can always be re-fetched, even across sessions.
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
TASK_IDS_PATH = OUTPUT_DIR / "llm_bo_interplay_task_ids.json"

POLL_INTERVAL_SECONDS = 30

# ---------------------------------------------------------------------------
# Queries. Each is written so the answer surfaces concrete, citable papers
# and, where possible, the open-source repositories that accompany them.
# ---------------------------------------------------------------------------

LLM_BO_INTERPLAY_QUERY = (
    "High-effort literature review of the INTERPLAY between large language "
    "models (LLMs) and Bayesian optimization (BO), separately or together, "
    "for materials discovery, chemistry, and related experimental-design "
    "tasks. Emphasize work from 2024-2026; earlier foundational papers are "
    "also welcome. Cover each of the following as a separate short "
    "subsection, and for EACH give the most relevant papers with FULL "
    "citations (authors, title, venue, year, DOI) plus the associated "
    "open-source code repository URL when one exists: "
    "(1) LLMs used directly as optimizers or experiment proposers in place "
    "of BO, and head-to-head comparisons of LLM-driven search versus "
    "classical BO; "
    "(2) hybrid LLM/BO frameworks in which LLM-generated hypotheses, "
    "domain knowledge, or priors warm-start or steer a BO campaign, "
    "including the Cooper group's Language-Based Bayesian Optimization "
    "Research Assistant (BORA, IJCAI 2025) and its follow-up study of "
    "reasoning models in closed-loop experiments (Digital Discovery, 2026, "
    "DOI 10.1039/D5DD00520E); "
    "(3) LLMs for BO problem setup: design-space specification, feature or "
    "descriptor selection, and constraint elicitation; "
    "(4) LLM-based or foundation-model-based surrogates and in-context "
    "regression used inside BO loops, including critical or 'sober' "
    "assessments of whether they beat strong classical baselines; "
    "(5) agentic and closed-loop laboratory systems that combine LLM "
    "planning with BO-driven experiment selection. "
    "Prefer chemistry and materials applications. Provide a consolidated "
    "reference list with DOIs at the end."
)

LLM_BO_REPOS_QUERY = (
    "Survey of open-source SOFTWARE REPOSITORIES (GitHub or similar) at the "
    "intersection of large language models (LLMs) and Bayesian optimization "
    "(BO) for chemistry, materials discovery, and experimental design, from "
    "2023-2026. For each tool or framework give: the repository name and "
    "URL, a one-sentence description of how it combines or compares LLMs "
    "and BO, and the associated paper with a FULL citation (authors, title, "
    "venue, year, DOI) when one exists. Include, where relevant: hybrid "
    "LLM+BO optimizers (e.g., BORA), LLM agents that orchestrate BO "
    "libraries such as BoTorch/Ax or BayBE, LLM-based surrogate or "
    "in-context regression tools, benchmark suites that pit LLMs against "
    "BO on optimization tasks, and LLM copilots for self-driving "
    "laboratories. Provide a consolidated list at the end."
)

COOPER_REASONING_QUERY = (
    "Focused literature review of Andrew I. Cooper's group (University of "
    "Liverpool) on combining large language models (LLMs) with Bayesian "
    "optimization (BO) for scientific discovery, 2024-2026. Two anchor "
    "papers: (a) Cisse, Evangelopoulos, Gusev, and Cooper, 'Language-Based "
    "Bayesian Optimization Research Assistant (BORA)', IJCAI 2025 "
    "(arXiv:2501.16224); and (b) Cisse, Cooper, Zhu, Evangelopoulos, and "
    "Cooper, 'Can we automate scientific reasoning in closed-loop "
    "experiments using large language models?', Digital Discovery, 2026, "
    "DOI 10.1039/D5DD00520E, which benchmarks reasoning models (e.g., o3, "
    "o4-mini, gpt-5, gemini-2.5-flash) as optimizers on a physics-based "
    "petanque simulation and a photocatalytic hydrogen-evolution problem "
    "and inspects their reasoning chains. For each anchor paper: summarize "
    "the method, the benchmark problems (including the petanque problem "
    "and the chemistry-specific tasks), the main quantitative findings on "
    "LLM/BO hybrids versus BO-only baselines, and what the reasoning-chain "
    "or commentary analysis revealed about how the LLMs 'think' during "
    "optimization. Then list follow-up, companion, or closely related "
    "works that cite or build on these two papers, with FULL citations "
    "(authors, title, venue, year, DOI) and code repository URLs where "
    "available."
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

    jobs = {
        "llm_bo_interplay": (JobNames.LITERATURE_HIGH, LLM_BO_INTERPLAY_QUERY),
        "llm_bo_repos": (JobNames.LITERATURE, LLM_BO_REPOS_QUERY),
        "cooper_llm_reasoning": (JobNames.LITERATURE, COOPER_REASONING_QUERY),
    }
    for label, (job_name, query) in jobs.items():
        task = TaskRequest(name=job_name, query=query)
        task_id = client.create_task(task)
        task_ids[label] = str(task_id)
        print(f"Submitted {job_name} [{label}]: {task_id}")

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
