# Follow-on work connected to the AC BO Hackathon 2024

Compiled for [issue #172](https://github.com/AC-BO-Hackathon/ac-bo-hackathon.github.io/issues/172), in support of
Referee 2's question on [PR #171](https://github.com/AC-BO-Hackathon/ac-bo-hackathon.github.io/pull/171) about
whether any follow-up study or downstream output exists. Event: 27–28 March 2024, Acceleration Consortium
(University of Toronto) with Merck KGaA, 45 team projects.

Evidence is graded, because "connected to the hackathon" spans everything from a paper that names the event in
its acknowledgements to a paper by the same people on the same topic that never mentions it. The distinction
matters for what the manuscript can claim.

Supporting data in [`edison_output/followon/`](edison_output/followon):
`repo_afterlife.json` (per-repository post-event activity), `arxiv_fulltext_sweep.json` (co-author arXiv
full-text sweep), and four Edison Scientific `LITERATURE_HIGH` answers.

---

## Tier A — explicit acknowledgement of the hackathon

Two works, one of them the hackathon manuscript itself.

| Work | Link to hackathon | Citation |
|---|---|---|
| **Ranking over regression for Bayesian optimization and molecule selection** | Acknowledgements: *"This project was also part of the Acceleration Consortium Bayesian optimization hackathon."* | Tom, Lo, Corapi, Aspuru-Guzik, Sanchez-Lengeling. *APL Machine Learning* **3**, 036113 (2025). [10.1063/5.0272663](https://doi.org/10.1063/5.0272663); [arXiv:2410.09290](https://arxiv.org/abs/2410.09290) |
| **Bayesian Optimization Hackathon for Chemistry and Materials** | The event's own proceedings preprint | Baird, Ansari, *et al.* ChemRxiv (2025). [10.26434/chemrxiv-2025-dzh5z](https://doi.org/10.26434/chemrxiv-2025-dzh5z) |

Tom et al. is **Project 44** (RBBO, `gkwt/rank-bo`) carried to a peer-reviewed journal by the same three
hackathon participants (Gary Tom, Stanley Lo, Samantha Corapi) plus two senior authors. It is the only
independent publication found anywhere that names the event.

Also in this tier by construction: `csmova/SeroOpt`, whose README credits hackathon **Projects 30 and 31** by
URL and points at the resulting paper — see Tier B.

## Tier B — same team, same project topic, no explicit credit

These are the projects that demonstrably continued. In every case the connection is the people plus the
research question, not a citation; none of these papers cites the hackathon (verified against their Crossref
reference lists).

| Proj. | Hackathon project | Follow-on work |
|---|---|---|
| 30, 31 | Active learning for voltammetry waveform design; ask/tell tutorial for Ax | Movassaghi *et al.*, **Machine-learning-guided design of electroanalytical pulse waveforms**, *Digital Discovery* **4**, 1812–1832 (2025), [10.1039/D5DD00005J](https://doi.org/10.1039/D5DD00005J). The [`csmova/SeroOpt`](https://github.com/csmova/SeroOpt) repository carries the paper's dataset ([10.5281/zenodo.15339008](https://doi.org/10.5281/zenodo.15339008)) and links both hackathon project pages |
| 21 | Benchmarking MolDAIS | Sorourifar, Banker, Paulson, **Adaptive subspace Bayesian optimization over molecular descriptor libraries**, *Digital Discovery* **4**, 2910–2926 (2025), [10.1039/D5DD00188A](https://doi.org/10.1039/D5DD00188A) |
| 36 | Scalable nonmyopic BO in dynamic cost settings | Truong, Nguyen, Neiswanger, **Griffiths**, Ermon, Haber, Koyejo, **Neural Nonmyopic Bayesian Optimization in Dynamic Cost Settings**, [arXiv:2601.06505](https://arxiv.org/abs/2601.06505) (2026). Same title and same two leads; Ryan-Rhys Griffiths (Project 35 lead) joins as a co-author |
| 45 | Bayesian Optimization for Generality | Schmid, Rajaonson, Ser, Haddadnia, Leong, Aspuru-Guzik, Kristiadi, Jorner, Strieth-Kalthoff, **Bayesian Optimization for General Reaction Conditions (CurryBO)**, [arXiv:2502.18966](https://arxiv.org/abs/2502.18966) (2025) — five of the six project-45 members. Also Haddadnia, Grashoff, Strieth-Kalthoff, **BoTier**, *Digital Discovery* **4**, 1417–1422 (2025), [10.1039/D5DD00039D](https://doi.org/10.1039/D5DD00039D) |
| 15 | Adaptive batch sizes for BO of reaction yield | Schoepfer, Weinreich, Laplaza, Waser, Corminboeuf, **Cost-informed Bayesian reaction optimization**, *Digital Discovery* **3**, 2289–2297 (2024), [10.1039/D4DD00225C](https://doi.org/10.1039/D4DD00225C) — three of the project's members, published seven months after the event |
| 14 | BO of likely negative candidates in imbalanced biological datasets | Caldas Ramos, Michtavy, White, Porosoff, **Bayesian Optimization of Catalysis with In-Context Learning**, *ACS Central Science* (2026), [10.1021/acscentsci.5c02418](https://doi.org/10.1021/acscentsci.5c02418) — same two leads, topic shifted from imbalanced-data BO to LLM-assisted BO |
| 24 | ScattBO benchmark | Anker *et al.*, **Autonomous nanoparticle synthesis by design** (ScatterLab), [arXiv:2505.13571](https://arxiv.org/abs/2505.13571) (2025) — the physical-lab realization of what ScattBO simulates. Connection is thematic; the preprint's abstract does not name ScattBO |
| 41 | RAMBO I (retrieval-augmented BO initialization) | Ranković, Schwaller, **GOLLuM: Gaussian Process Optimized LLMs**, [arXiv:2504.06265](https://arxiv.org/abs/2504.06265) (2025) — same pair, continues the LLM-plus-BO line rather than RAMBO specifically. Its only "hackathon" mention is a citation to the LLM hackathon paper |
| 34 | BO in thermal fluid mixtures | Rajabi-Kochi, Mahboubi, Gill, Moosavi, **Adaptive representation of molecules and materials in Bayesian optimization**, *Chemical Science* (2025), [10.1039/D5SC00200A](https://doi.org/10.1039/D5SC00200A) — two of the project's members; weaker link than the rows above |

## Tier C — tools that were used at the hackathon and later published

The connection here runs through the software, not through a project team. Useful as evidence the hackathon
sat in an active tooling ecosystem; not evidence the hackathon produced the work.

- **BayBE** (Projects 7 and 26): Fitzner, Šošić, Hopp, Müller, Rihana *et al.*, *Digital Discovery* (2025),
  [10.1039/D5DD00050E](https://doi.org/10.1039/D5DD00050E). Five of the seven Merck project-26 members are
  authors, but BayBE predates the event.
- **Honegumi** (hackathon tooling by S. Baird): *npj Computational Materials* (2026),
  [10.1038/s41524-026-02156-0](https://doi.org/10.1038/s41524-026-02156-0), plus the *Honegumi RAG Assistant*
  preprint, [10.26434/chemrxiv-2025-f1wcr](https://doi.org/10.26434/chemrxiv-2025-f1wcr).
- **GAUCHE** (Project 35's tutorial subject): NeurIPS 36 (2023) — predates the hackathon.
- **Anubis** (Hickman, **Tom**, **Zou**, Aldeghi, Aspuru-Guzik), *Digital Discovery* (2025),
  [10.1039/D5DD00018A](https://doi.org/10.1039/D5DD00018A) — two participants, unrelated to their projects.

## Tier D — the event format itself propagating

- **2024 KRICT ChemDX Hackathon** (Yoo, Low *et al.*, *J. Mater. Inf.* **5**, 54 (2025),
  [10.20517/jmi.2025.65](https://doi.org/10.20517/jmi.2025.65)) cites both the hackathon **agenda page** and the
  proceedings preprint while surveying online/hybrid hackathon models. This is the only external paper found
  that cites the hackathon at all, and it cites it as an organizational precedent.
- **AC Hardware Hackathon 2024** ([`AC-Hardware-Hackathon/ac-hardware-hackathon.github.io`](https://github.com/AC-Hardware-Hackathon/ac-hardware-hackathon.github.io),
  May 2024) is a fork of this website, reusing the project-page and submission machinery — including several
  AC-BO project files still present in its tree.
- Two further forks became other events' sites: [`MQS-mark/Quantum_Challenge`](https://github.com/MQS-mark/Quantum_Challenge)
  → [`Quantum-Innovation-Challenge`](https://github.com/Quantum-Innovation-Challenge/quantum-innovation-challenge.github.io)
  (active to May 2026) and [`BII-Quantum/bii-quantum.github.io`](https://github.com/BII-Quantum/bii-quantum.github.io).
  The website has **62 forks** in total.
- [`KalininGroup/mic-hackathon`](https://github.com/KalininGroup/mic-hackathon) (microscopy ML hackathon,
  published as Pratiush *et al.*, *Mach. Learn.: Sci. Technol.* (2025),
  [10.1088/2632-2153/ae1f5d](https://doi.org/10.1088/2632-2153/ae1f5d)) references AC-BO-Hackathon in its
  repository, though its paper does not cite the event.

## Repository afterlife

From [`repo_afterlife.json`](edison_output/followon/repo_afterlife.json) — 45 projects, 40 listing a repository
(39 unique; projects 30 and 31 share one), 34 still reachable:

- **28 repositories** received at least one commit on or after 29 March 2024 (the day after the event closed),
  but most of that is same-week cleanup: only **8** were touched after 30 April 2024, and only **one** after
  December 2024.
- Longest-running: `AC-BO-Hackathon/BOPE-GPT` (92 commits, to Dec 2024, with a deployed app),
  `AndySAnker/ScattBO` (72 commits, to Nov 2024), `AC-BO-Hackathon/project-AiChemMcGill` (to Jan 2025 — the
  last commit anywhere in the cohort).
- Most-starred: `leojklarner/gauche` (256★, pre-existing library),
  `materials-data-facility/awesome-bayesian-optimization` (54★),
  `AC-BO-Hackathon/project-surface-science-syndicate` (9★), `janweinreich/best_batchers` (9★),
  `FrankWanger/ACBO-Feat` (7★), `schwallergroup/rambo-I` (7★).
- **5 listed repositories are now unreachable** (deleted, renamed, or made private): projects 9, 21, 36, 40 and
  45; project 42's link pointed at a fork of this website that its owner has since renamed. Notably, projects
  21, 36 and 45 are three of the strongest Tier-B cases — the work continued, but under a new repository
  elsewhere.
- **No releases** across the reachable project repositories except `danieleongari/blends` (1).

## Method, and what it does not cover

1. **Edison Scientific** — four `LITERATURE_HIGH` (PaperQA) tasks via
   [`scripts/edison_followon_search.py`](scripts/edison_followon_search.py): works acknowledging/citing the
   event; a project-by-project follow-up sweep over all 45 titles; downstream uptake of the seven named
   artifacts; and a re-run of the first query with the corrected event dates and a known-positive example
   supplied. Raw answers are archived alongside the script.
2. **arXiv full-text sweep** — the strongest negative evidence here. For each of the 126 manuscript
   co-authors, every arXiv submission on/after 25 March 2024 was collected (400 unique papers), 374 full texts
   were retrieved and grepped for "hackathon". Exactly **one** hit credits this event (Tom et al.); the other
   three are the 2023/2024/2025 LLM hackathon papers.
3. **GitHub** — metadata and post-event commit history for all 40 project repositories; global code and
   repository search for references to the org; fork network of the website.
4. **Bibliographic** — OpenAlex (works citing the preprint and the Zenodo records; per-participant works since
   April 2024), Crossref (DOI verification and reference-list checks for hackathon citations), Zenodo, Europe
   PMC full-text search.

Not covered, and worth stating plainly:

- **Google Scholar profiles could not be read directly** — Scholar blocks automated access. Co-author output
  was instead enumerated through OpenAlex and the arXiv author sweep above, which covers preprints and indexed
  journal articles but will miss theses, talks, patents, and Scholar-only entries.
- **ChemRxiv is behind Cloudflare** and RSC/ScienceDirect return 403 to automated fetches, so non-arXiv full
  texts could not be grepped for acknowledgements; for those, reference lists were checked via Crossref
  instead, which catches citations but not prose acknowledgements. A Tier-A acknowledgement hiding in a
  journal-only paper would therefore have been missed.
- **Absence of evidence in Tier A is partly an artefact of practice** — participants continued the work but
  did not credit the event. That is itself the finding: the hackathon's outputs are traceable through people
  and repositories, not through citations.
