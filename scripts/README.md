# Scripts

## `edison_suggest_reviewers.py`

Uses the [Edison Scientific](https://docs.edisonscientific.com/) `edison-client`
API to suggest potential peer reviewers for the manuscript (`main.tex` /
`copilot-main-fixed.pdf`).

It runs two jobs concurrently:

1. **`ANALYSIS`** — the manuscript is uploaded and attached as a file, and the
   agent is asked to propose a ranked list of potential reviewers (with
   affiliations, expertise, representative papers, and conflicts of interest to
   exclude).
2. **`LITERATURE_HIGH`** — a high-effort literature query on the manuscript's
   topic to surface closely related work and prominent, active authors who would
   be strong reviewer candidates.

### Run

```bash
pip install edison-client
export EDISON_API_KEY=...        # your Edison Scientific API key
                                # (EDISON_PLATFORM_API_KEY is also accepted)
python scripts/edison_suggest_reviewers.py
```

Results are written to `edison_output/`: `analysis_answer.md` (the ranked
reviewer suggestions), `literature_answer.md` (the high-effort literature
review), `task_ids.json` (so the jobs can be re-fetched later), and a local-only
analysis notebook (`*_notebook.ipynb`, git-ignored).

A completed run is committed under `edison_output/` for reference.

Run `python scripts/edison_suggest_reviewers.py --help` for all options
(`--manuscript`, `--output-dir`, `--continued-job-id`, `--timeout`,
`--no-analysis`, `--no-literature`).

> **Note:** This requires outbound network access to the Edison API
> (`api.platform.edisonscientific.com`) and a valid `EDISON_API_KEY` (or
> `EDISON_PLATFORM_API_KEY`).
