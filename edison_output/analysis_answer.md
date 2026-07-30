I read the manuscript and screened candidate reviewers against the visible author list and affiliations in the PDF. Below is a ranked list of 15 potential reviewers for a journal like *Digital Discovery*, focused on Bayesian optimization, active learning, self-driving labs, and ML for chemistry/materials. I explicitly excluded apparent conflicts of interest from the manuscript author list, same-institution candidates, and a few very likely close-collaborator cases.

## Recommended reviewer shortlist

| Rank | Candidate | Current affiliation | Public email/profile | Relevant expertise | Representative recent publications (1–3) |
|---|---|---|---|---|---|
| 1 | **Roman Garnett** | Washington University in St. Louis | https://www.cse.wustl.edu/~garnett/ | Bayesian optimization, Gaussian processes, active learning; broad BO perspective well matched to a methods-and-community manuscript | **Bayesian Optimization** (book, Cambridge Univ. Press, 2023); **Bayesian optimization of function networks with partial evaluations** (2023/2024 preprint); BO and decision-making work listed on lab page |
| 2 | **Peter I. Frazier** | Cornell University, School of Operations Research and Information Engineering | https://people.orie.cornell.edu/pfrazier/ | Foundational Bayesian optimization, multi-information source optimization, sequential decision-making | Poloczek, Wang & Frazier, **Multi-information source optimization** (NeurIPS 2017); Lin, Astudillo, Frazier & Bakshy, **Preference exploration for efficient Bayesian optimization with multiple outcomes** (AISTATS 2022); recent BO papers on his publications page |
| 3 | **José Miguel Hernández-Lobato** | University of Cambridge | https://jmhl.org/ | Bayesian optimization, probabilistic ML, molecule-design BO, active learning | **Diagnosing and fixing common problems in Bayesian optimization for molecule design** (OpenReview/2024); García-Ortegón et al., **Docking scores, Bayesian optimization and the trade-off between exploration and exploitation in de novo drug design** (2021); profile/publications at jmhl.org |
| 4 | **Maximilian Balandat** | Meta | https://botorch.org/ | BoTorch, Monte Carlo Bayesian optimization, multi-objective and noisy BO; very relevant to many hackathon projects discussed in the manuscript | Balandat et al., **BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization** (NeurIPS 2020); Daulton, Balandat & Bakshy, **Parallel Bayesian Optimization of Multiple Noisy Objectives with Expected Hypervolume Improvement** (NeurIPS 2021); BoTorch project/publication pages |
| 5 | **Frank Hutter** | University of Freiburg / ELLIS Institute Tübingen | https://ml.informatik.uni-freiburg.de/profile/hutter/ | Hyperparameter optimization, Bayesian optimization, benchmarking, AutoML; useful for judging BO benchmarking/tutorial content | Lindauer et al., **SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization** (JMLR/2022 or 2023 package paper); broad HPO/BO benchmark work on lab page; recent AutoML optimization papers listed at Freiburg profile |
| 6 | **Marius Lindauer** | Leibniz University Hannover | https://www.ai.uni-hannover.de/en/lindauer | Bayesian optimization for hyperparameter optimization, benchmarking, reproducibility in optimization workflows | **SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization** (OpenReview/JMLR track, 2023); recent AutoML and optimization benchmarking papers on Hannover profile |
| 7 | **Aaron Gilad Kusne** | National Institute of Standards and Technology (NIST) | https://www.nist.gov/people/aaron-gilad-kusne | Autonomous materials research systems, closed-loop materials discovery, Bayesian active learning | Kusne et al., **On-the-fly closed-loop materials discovery via Bayesian active learning** (Nature Communications, 2020); Leeman et al., **Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis** (PRX Energy, 2024); NIST AMRS profile |
| 8 | **Milad Abolhasani** | North Carolina State University | https://cbe.ncsu.edu/people/mabolha/ | Self-driving laboratories, autonomous experimentation, closed-loop optimization in chemistry/materials | Recent self-driving lab publications listed on lab page; autonomous experimentation papers from Abolhasani lab in flow chemistry/materials; profile at NCSU and https://www.abolhasanilab.com/ |
| 9 | **Keith A. Brown** | Boston University | https://www.bu.edu/eng/profile/keith-brown/ | Self-driving labs, autonomous experiments, ML-guided materials discovery; very strong fit for the hackathon/community angle | **Superlative mechanical energy absorbing efficiency discovered through self-driving lab-human partnership** (Nature Communications, 2024); recent autonomous materials experimentation papers on KABlab site |
| 10 | **Pascal Friederich** | Karlsruhe Institute of Technology (KIT) | https://www.aimat.iar.kit.edu/index.php | ML for materials and molecules, active learning, autonomous/discovery pipelines in chemistry and materials | Recent active-learning and molecular/materials ML work listed through KIT AiMat pages; e.g. **Conditional Normalizing Flows for Active Learning of Coarse-Grained Molecular Representations** (2024 preprint); related materials ML publications on KIT profile |
| 11 | **Olexandr Isayev** | Carnegie Mellon University | https://olexandrisayev.com/ | AI for chemistry, molecular optimization, active learning, generative design | Recent molecular design and active-learning papers on lab page; work on sampling chemical space and catalyst development by active learning; CMU faculty page |
| 12 | **Ekin D. Cubuk** | Google DeepMind | Nature paper/profile entry via search: https://www.nature.com/articles/s41586-023-06735-9 | ML for materials discovery at scale; broader materials-AI reviewer for benchmark/community significance | Merchant et al., **Scaling deep learning for materials discovery** (*Nature*, 2023); related materials discovery work through DeepMind publications |
| 13 | **Helge Stein** | Technical University of Munich | https://www.ch.nat.tum.de/digicat/team/helge-stein/ | Autonomous laboratories, battery/materials optimization, digital catalysis | TUM profile and recent autonomous battery/self-driving lab publications; **Robotic cell assembly to accelerate battery research** (2023/2024-related TUM/KIT output) |
| 14 | **Edward O. Pyzer-Knapp** | IBM Research | IBM publications page: https://research.ibm.com/publications?author=18779 | ML for chemistry/materials, inverse design, active learning, industrial digital discovery | Recent IBM materials/chemistry ML papers listed on IBM page; long-standing fit for Digital Discovery-style work |
| 15 | **Linda Hung** | Toyota Research Institute | http://www.tri.global/about-us/dr-linda-hung | Materials informatics, high-throughput computational materials design, AI for materials discovery | TRI profile and recent materials-AI publications on profile/Scholar; strong materials-discovery perspective for judging benchmark relevance |

## Short justifications for the top-ranked candidates

1. **Roman Garnett**: Probably the cleanest fit if you want someone respected across BO theory and practice, but not obviously entangled with the author list. His BO book also makes him a good judge of the manuscript’s tutorial, benchmarking, and community-building aspects.
2. **Peter Frazier**: Foundational BO researcher whose work directly overlaps multi-fidelity, preference, and sequential optimization themes appearing in the manuscript.
3. **José Miguel Hernández-Lobato**: Strong match to BO for molecule design and practical failure modes in scientific BO, which is close to the manuscript’s chemistry/materials scope.
4. **Maximilian Balandat**: Extremely relevant because the manuscript discusses BoTorch-based benchmarking and multi-objective acquisition functions. He would be technically strong on BO implementation and evaluation.
5. **Frank Hutter**: Good choice if the editor wants a reviewer with strong instincts for optimization benchmarking, software ecosystems, and reproducibility.
6. **Marius Lindauer**: Similar strengths to Hutter, with particular usefulness for judging benchmark fairness, software comparisons, and practical optimizer evaluation.
7. **Aaron Gilad Kusne**: Best fit from the autonomous materials / closed-loop experimentation side.
8. **Milad Abolhasani**: Strong self-driving lab perspective, especially if the editor wants a reviewer who can assess the manuscript’s community impact for autonomous experimentation.
9. **Keith Brown**: Very relevant for self-driving labs in materials and human-in-the-loop autonomous experimentation.
10. **Pascal Friederich**: Good bridge reviewer between ML methodology and chemistry/materials application.

## Likely conflicts of interest explicitly excluded

I excluded these categories based on the manuscript author list and affiliations visible in the PDF:

- **All manuscript co-authors**: this includes, for example, Sterling G. Baird, Taylor Sparks, Philippe Schwaller, Ryan-Rhys Griffiths, Raul Astudillo, and all other named authors on pages 1–2 of the manuscript.
- **Same-institution candidates as author affiliations**: I excluded likely candidates from institutions already on the paper, including **University of Toronto / Acceleration Consortium, Merck KGaA, MIT, EPFL, University of Utah, McGill, UCL, Ohio State, University of Chicago, Stanford, Princeton, Imperial College London, Johns Hopkins, UCLA, DTU, University of Washington, University of Manchester, KAIST, University of Edinburgh**, and others listed in the author affiliations.
- **Examples of specifically excluded otherwise-relevant names**:
  - **Antonio “Tonio” Buonassisi** — excluded because **MIT** appears among manuscript author affiliations.
  - **Connor Coley, Rafael Gómez-Bombarelli, Heather Kulik, Klavs Jensen** — excluded on the same **MIT** basis.
  - **Andrew White** and **Kevin Jablonka** — not manuscript co-authors here, but I flagged them as **likely too close to this community/hackathon orbit** given the cited prior LLM hackathon paper with overlap in organizers/participants, so I did not recommend them.
  - **Berend Smit** — excluded because **EPFL** appears in the author list.
  - **John Gregoire** — excluded because **Caltech** appears in the author list.
  - **Sergei Kalinin** — excluded because **University of Tennessee** appears in the author list.

## Notes and limitations

- I used the manuscript PDF itself to identify co-authors and same-institution conflicts.
- For publications and affiliations, I relied on public institutional/profile pages and search results. Some candidates do not expose a public email, so I provided a stable profile URL instead.
- I cannot guarantee detection of all **close-collaborator** conflicts without a full co-authorship/network analysis over recent years. I therefore treated obvious same-paper, same-institution, and highly visible community-overlap cases conservatively.
- If you want, I can turn this into a tighter **editor-ready 10-person shortlist** with a balance across **BO theory / chemical ML / self-driving labs / materials informatics**.

**Discretionary analytical decisions**
- Ranked candidates by a mix of topical fit, seniority, breadth across BO and self-driving labs, and apparent distance from the author list.
- Treated **same institution as any manuscript author** as a hard exclusion criterion.
- Treated a small number of **likely very close collaborator / same-community-organizer** cases as exclusions even without identical institution.
- Preferred candidates with a **public institutional profile URL** when public email was not readily available.
- Allowed a few reviewers from **industry research labs** (Meta, Google DeepMind, IBM, TRI) because the manuscript spans academia-industry-community benchmarking and Digital Discovery often uses such reviewers.
- Kept **Maximilian Balandat** despite strong topical overlap with cited BoTorch work because I found no direct co-authorship or same-institution conflict from the manuscript author list; editors may still prefer him slightly lower if they want more distance from core software cited in the paper.