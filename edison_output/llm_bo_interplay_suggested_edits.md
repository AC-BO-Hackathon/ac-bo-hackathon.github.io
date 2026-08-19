# Suggested manuscript edits: LLM / BO interplay citations (issue #173)

Prepared for PR #171 (`copilot/address-dd-reviewer-feedback`). Sources: the three
Edison answers in this folder (`llm_bo_interplay_answer.md`,
`llm_bo_repos_answer.md`, `cooper_llm_reasoning_answer.md`), cross-checked
against Crossref, arXiv, and the Cooper group's announcement page. Task IDs are
in `llm_bo_interplay_task_ids.json` for re-fetching.

## Where to insert

Primary location: `main.tex`, Future Opportunities section (`\label{sec:future}`),
in the paragraph that begins "The large share of hackathon projects that already
incorporated language models points to \emph{foundation-model- and LLM-assisted
BO} as a particularly active frontier". On the PR branch this sentence currently
ends with `~\cite{kristiadi_sober_2024, rankovic_gollum_2025}.` Insert the new
text immediately after that sentence, before "Other opportunities include".

Secondary option (lighter touch): append `cisse_reasoning_2026` to the citation
list at the end of the LLM sentence in the "Scientific lessons" subsection
(the sentence ending `...requires validation against non-LLM
baselines~\cite{kristiadi_sober_2024}.`), since that paper's control studies
are exactly about validating LLM optimizers against non-LLM baselines.

## Suggested LaTeX (preferred, two sentences)

```latex
Hybrid designs from the Cooper group illustrate this frontier concretely:
BORA couples an LLM that warm-starts the search with diverse hypotheses, and
that intervenes when progress stalls, to a Gaussian-process surrogate that
retains uncertainty-driven control of the campaign, outperforming BO-only and
LLM-only baselines on tasks that include a physics-based p\'etanque game and
photocatalytic hydrogen production~\cite{cisse_bora_2025}. A follow-up study
in this journal benchmarked frontier reasoning models as closed-loop
optimizers on the same p\'etanque and hydrogen-evolution problems and
inspected their reasoning chains directly, finding that LLM/BO hybrids excel
at early-stage exploration and that LLM-only optimizers can sometimes win,
while control studies exposed clear limitations of purely language-driven
search~\cite{cisse_reasoning_2026}.
```

## Suggested LaTeX (minimal, one sentence)

```latex
Recent work from the Cooper group exemplifies this direction, first coupling
dynamically revised LLM hypotheses with GP-based search
(BORA)~\cite{cisse_bora_2025} and then benchmarking frontier reasoning models
in closed-loop experiments on physics-based (p\'etanque) and photocatalytic
hydrogen-evolution problems while inspecting their reasoning
chains~\cite{cisse_reasoning_2026}.
```

## BibTeX entries (add to `latex/references.bib`)

Verified against Crossref (titles, authors, volume/pages, DOIs).

```bibtex
@inproceedings{cisse_bora_2025,
	title = {Language-{Based} {Bayesian} {Optimization} {Research} {Assistant} ({BORA})},
	author = {Cissé, Abdoulatif and Evangelopoulos, Xenophon and Gusev, Vladimir V. and Cooper, Andrew I.},
	booktitle = {Proceedings of the {Thirty}-{Fourth} {International} {Joint} {Conference} on {Artificial} {Intelligence} ({IJCAI}-25)},
	pages = {4967--4975},
	year = {2025},
	doi = {10.24963/ijcai.2025/553},
	url = {https://doi.org/10.24963/ijcai.2025/553},
}

@article{cisse_reasoning_2026,
	title = {Can we automate scientific reasoning in closed-loop experiments using large language models?},
	author = {Cissé, Abdoulatif and Cooper, Max E. and Zhu, Mengjia and Evangelopoulos, Xenophon and Cooper, Andrew I.},
	journal = {Digital Discovery},
	volume = {5},
	pages = {1132--1160},
	year = {2026},
	doi = {10.1039/D5DD00520E},
	url = {https://doi.org/10.1039/D5DD00520E},
}
```

## Fact notes for the two anchor papers

- BORA (IJCAI 2025, arXiv:2501.16224): GP with Matern kernel and expected
  improvement; GPT-4o-mini generates warm-start hypotheses, live commentary,
  and plateau-triggered proposals under an adaptive trust policy. Benchmarks:
  Branin 2D, Levy 10D, Ackley 15D, solar energy 4D, petanque 7D, sugar beet
  8D, photocatalytic hydrogen production 10D (the constrained mixture setting
  from the Liverpool mobile robotic chemist). Beat ColaBO on 5 of 6 tasks,
  significant vs HypBO (p = 0.02), early petanque gain of about 35 points from
  LLM hypotheses, and up to 67% improvement over an LLM-only optimizer on
  hydrogen production. Key qualitative finding: LLM-only search is competitive
  early but stagnates without BO's uncertainty-driven exploration.
- Reasoning study (Digital Discovery, 2026, 5, 1132-1160, DOI
  10.1039/D5DD00520E; ChemRxiv preprint 10.26434/chemrxiv.10001632/v2;
  published 23 Feb 2026): benchmarks five reasoning models (o3, o4-mini,
  gpt-5, gpt-5-mini, gemini-2.5-flash) as optimizers on a 7D physics-based
  petanque simulation and a 10D photocatalytic hydrogen-evolution problem,
  with explicit inspection of reasoning chains. Hybrids of BO and LLMs
  navigate high-dimensional chemical space well and are strongest in
  early-stage exploration; in some cases LLM-only optimizers outperform BO or
  the hybrids; o3 was the strongest and most consistent model after 150
  experiments; control studies probe the limitations of LLM-based methods.
  Note for the manuscript: this paper is in Digital Discovery itself, and the
  senior author is Andrew I. Cooper (co-author Max E. Cooper).

## Optional supporting citations

These strengthen the same paragraph if more breadth is wanted; all verified
against Crossref or the arXiv API. Full context in
`llm_bo_interplay_answer.md`.

```bibtex
@article{macknight_pretrained_2025,
	title = {Pre-trained knowledge elevates large language models beyond traditional chemical reaction optimizers},
	author = {MacKnight, Robert and Regio, Jose Emilio and Ethier, Jeffrey G. and Baldwin, Luke A. and Gomes, Gabe},
	journal = {arXiv},
	year = {2025},
	doi = {10.48550/arXiv.2509.00103},
	url = {https://doi.org/10.48550/arXiv.2509.00103},
}

@article{chang_llinbo_2025,
	title = {{LLINBO}: {Trustworthy} {LLM}-in-the-{Loop} {Bayesian} {Optimization}},
	author = {Chang, Chih-Yu and Azvar, Milad and Okwudire, Chinedum and Al Kontar, Raed},
	journal = {arXiv},
	year = {2025},
	doi = {10.48550/arXiv.2505.14756},
	url = {https://doi.org/10.48550/arXiv.2505.14756},
}

@article{ramos_incontext_2026,
	title = {Bayesian {Optimization} of {Catalysis} with {In}-{Context} {Learning}},
	author = {Ramos, Mayk Caldas and Michtavy, Shane S. and White, Andrew D. and Porosoff, Marc D.},
	journal = {ACS Central Science},
	volume = {12},
	pages = {599--615},
	year = {2026},
	doi = {10.1021/acscentsci.5c02418},
	url = {https://doi.org/10.1021/acscentsci.5c02418},
}

@article{wang_trainingfree_2026,
	title = {Training-free active learning framework in materials science with large language models},
	author = {Wang, Hongchen and Espinosa Castañeda, Rafael and Werber, Jay R. and Fehlis, Yao and Kim, Edward and Hattrick-Simpers, Jason},
	journal = {npj Computational Materials},
	volume = {12},
	year = {2026},
	doi = {10.1038/s41524-026-02136-4},
	url = {https://doi.org/10.1038/s41524-026-02136-4},
}
```

Example use of the optional set, extending the preferred insertion:

```latex
Head-to-head comparisons now cut both ways: frontier LLMs can match or beat
classical BO on enumerated categorical reaction spaces~\cite{macknight_pretrained_2025}
and training-free LLM active learning can converge faster than surrogate-based
baselines~\cite{wang_trainingfree_2026}, while in-context LLM surrogates
performed on par with Gaussian processes in real catalysis
campaigns~\cite{ramos_incontext_2026} and theoretically grounded hybrids
provide regret guarantees for LLM-in-the-loop designs~\cite{chang_llinbo_2025}.
```

## Notable repositories surfaced (details in `llm_bo_repos_answer.md`)

- LLM4BO, https://github.com/learningmatter-mit/LLM4BO (Gomez-Bombarelli
  group benchmark of LLM vs statistical BO for biochemical discovery)
- LLM-in-the-Loop-BO, https://github.com/UMDataScienceLab/LLM-in-the-Loop-BO
  (LLINBO)
- OptFormer Embed-then-Regress,
  https://github.com/google-research/optformer/tree/main/optformer/embed_then_regress
- Coscientist, https://github.com/gomesgroup/coscientist (LLM agent compared
  against BO on reaction optimization)
- OPRO, https://github.com/google-deepmind/opro (foundational LLMs-as-optimizers)
- BORA code link given in the paper: https://anonymous.4open.science/r/bora-the-explorer
