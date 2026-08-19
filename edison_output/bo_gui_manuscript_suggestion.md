# Suggested manuscript additions: accessible interfaces for Bayesian optimization

Supports issue #174 and the Digital Discovery revision in PR #171. Sources: the three
Edison Scientific answers archived in this directory (`bo_gui_tools_answer.md`,
`bo_joss_gui_answer.md`, `bo_deployability_answer.md`). All DOIs below were verified
against the Crossref API on 2026-08-19.

## 1. Primary insertion: end of "Scientific lessons" subsection in `main.tex`

Location: append as a new final paragraph of
`\subsection{Scientific lessons: strengths and limitations of Bayesian optimization}`
(label `sec:sci-lessons`), after the paragraph that ends with "not benchmark verdicts."
This is the subsection the response letter already points to for Referee 1, point 2
("Are BO tools going to be easily deployable in experimental data settings?").

```latex
% Accessible interfaces for BO (Referee 1, point 2: deployability in experimental settings)
On the related question of whether \gls{bo} tools are easily deployable in experimental settings, the tooling ecosystem has advanced rapidly on the interface side. Beyond code-first libraries, experimentalists can now start from interactive template generators such as Honegumi, which produces unit-tested, Ax-based scripts from a point-and-click grid~\cite{baird_honegumi_2026}; no-install web applications such as the multi-objective EDBO+ app, Web-BO, and OPTIMEO~\cite{torres_multiobjective_2022, mroz_webbo_2025, bousige_optimeo_2025}; desktop applications such as BOXVIA and MADGUI~\cite{ishii_boxvia_2022, bajan_madgui_2025}; and web-based orchestration layers with built-in \gls{bo} for automated laboratories, such as NIMS-OS and IvoryOS~\cite{tamura_nimsos_2023, zhang_ivoryos_2025}. These interfaces largely remove the coding barrier; the harder parts of deployment now lie in problem formulation, instrument integration, and data infrastructure~\cite{seifrid_autonomous_2022}.
```

## 2. Secondary tweak: "Future Opportunities" section in `main.tex`

In the final paragraph of `\section{Future Opportunities}` (label `sec:future`), extend
the deployment-ready-tooling clause.

Before:

```latex
and \emph{domain-specific, deployment-ready BO tools} for synthesis and processing optimization that meet experimentalists where they work~\cite{durholt_bofire_2024, fitzner_baybe_2022}.
```

After:

```latex
and \emph{domain-specific, deployment-ready BO tools} for synthesis and processing optimization that meet experimentalists where they work, increasingly through no-code and low-code interfaces~\cite{durholt_bofire_2024, fitzner_baybe_2022, baird_honegumi_2026, mroz_webbo_2025, bousige_optimeo_2025}.
```

## 3. Response letter: `RESPONSE_TO_REVIEWERS.md`, Referee 1, point 2

Append to the existing answer:

> The revised Scientific lessons subsection now also surveys the accessible-interface
> ecosystem that has grown around this question: template generators (Honegumi, npj
> Computational Materials 2026), no-install web apps (EDBO+, Web-BO, and the
> JOSS-reviewed OPTIMEO), desktop GUIs (BOXVIA, MADGUI), and GUI-equipped laboratory
> orchestration (NIMS-OS, IvoryOS), with eight new references. These tools lower the
> coding barrier considerably; problem formulation and instrument and data integration
> remain the dominant deployment gaps.

## 4. New entries for `latex/references.bib`

All fields verified via Crossref except where noted. Honegumi volume and article number
were not yet indexed by Crossref at the time of writing; fill them in once available.

```bibtex
@article{baird_honegumi_2026,
	author = {Baird, Sterling G. and Falkowski, Andrew R. and Sparks, Taylor D.},
	title = {Honegumi: An Interface for Accelerating the Adoption of Bayesian Optimization in the Experimental Sciences},
	journal = {npj Computational Materials},
	year = {2026},
	doi = {10.1038/s41524-026-02156-0},
}

@article{torres_multiobjective_2022,
	author = {Torres, Jose Antonio Garrido and Lau, Sii Hong and Anchuri, Pranay and Stevens, Jason M. and Tabora, Jose E. and Li, Jun and Borovika, Alina and Adams, Ryan P. and Doyle, Abigail G.},
	title = {A Multi-Objective Active Learning Platform and Web App for Reaction Optimization},
	journal = {Journal of the American Chemical Society},
	volume = {144},
	number = {43},
	pages = {19999--20007},
	year = {2022},
	doi = {10.1021/jacs.2c08592},
}

@article{mroz_webbo_2025,
	author = {Mroz, Austin M. and Toka, Piotr N. and del R{\'i}o Chanona, Ehecatl Antonio and Jelfs, Kim E.},
	title = {Web-{BO}: towards increased accessibility of {Bayesian} optimisation ({BO}) for chemistry},
	journal = {Faraday Discussions},
	volume = {256},
	pages = {221--234},
	year = {2025},
	doi = {10.1039/D4FD00109E},
}

@article{bousige_optimeo_2025,
	author = {Bousige, Colin},
	title = {{OPTIMEO}: {Bayesian} Optimization Web App for Process Tuning, Modeling, and Orchestration},
	journal = {Journal of Open Source Software},
	volume = {10},
	number = {115},
	pages = {8510},
	year = {2025},
	doi = {10.21105/joss.08510},
}

@article{ishii_boxvia_2022,
	author = {Ishii, Akimitsu and Kamijyo, Ryunosuke and Yamanaka, Akinori and Yamamoto, Akiyasu},
	title = {{BOXVIA}: {Bayesian} optimization executable and visualizable application},
	journal = {SoftwareX},
	volume = {18},
	pages = {101019},
	year = {2022},
	doi = {10.1016/j.softx.2022.101019},
}

@article{bajan_madgui_2025,
	author = {Bajan, Christophe and Lambard, Guillaume},
	title = {{MADGUI}: Multi-Application Design Graphical User Interface for active learning assisted by {Bayesian} optimization},
	journal = {Chemometrics and Intelligent Laboratory Systems},
	volume = {258},
	pages = {105323},
	year = {2025},
	doi = {10.1016/j.chemolab.2025.105323},
}

@article{tamura_nimsos_2023,
	author = {Tamura, Ryo and Tsuda, Koji and Matsuda, Shoichi},
	title = {{NIMS-OS}: an automation software to implement a closed loop between artificial intelligence and robotic experiments in materials science},
	journal = {Science and Technology of Advanced Materials: Methods},
	volume = {3},
	number = {1},
	pages = {2232297},
	year = {2023},
	doi = {10.1080/27660400.2023.2232297},
}

@article{zhang_ivoryos_2025,
	author = {Zhang, Wenyu and Hao, Lucy and Lai, Veronica and Corkery, Ryan and Jessiman, Jacob and Zhang, Jiayu and Liu, Junliang and Sato, Yusuke and Politi, Maria and Reish, Matthew E. and Greenwood, Rebekah and Depner, Noah and Min, Jiyoon and El-khawaldeh, Rama and Prieto, Paloma and Trushina, Ekaterina and Hein, Jason E.},
	title = {{IvoryOS}: an interoperable web interface for orchestrating {Python}-based self-driving laboratories},
	journal = {Nature Communications},
	volume = {16},
	pages = {5182},
	year = {2025},
	doi = {10.1038/s41467-025-60514-w},
}

@article{seifrid_autonomous_2022,
	author = {Seifrid, Martin and Pollice, Robert and Aguilar-Granda, Andr{\'e}s and Morgan Chan, Zamyla and Hotta, Kazuhiro and Ser, Cher Tian and Vestfrid, Jenya and Wu, Tony C. and Aspuru-Guzik, Al{\'a}n},
	title = {Autonomous Chemical Experiments: Challenges and Perspectives on Establishing a Self-Driving Lab},
	journal = {Accounts of Chemical Research},
	volume = {55},
	number = {17},
	pages = {2454--2466},
	year = {2022},
	doi = {10.1021/acs.accounts.2c00220},
}
```

## 5. Additional tools surfaced but not proposed for citation

Kept out of the manuscript to limit citation growth; available if reviewers ask for
more breadth. Details and DOIs are in the archived Edison answers.

- AutoOED (desktop GUI, multi-objective; arXiv 2021, 10.48550/arXiv.2104.05959)
- CIME4R (web dashboard for analyzing reaction-optimization campaigns; J. Cheminformatics 2024, 10.1186/s13321-024-00840-1)
- Bgolearn/BgoFace (Python library plus GUI for materials; reported as npj Computational Materials 2026, DOI currently resolves to a Research Square preprint, 10.21203/rs.3.rs-8665853/v1)
- ProcessOptimizer (low-code ask/tell API; JCIM 2025, 10.1021/acs.jcim.4c02240)
- NEXTorch (low-code BoTorch toolkit with visualization; JCIM 2021, 10.1021/acs.jcim.1c00637)
- BOA (low-code, language-agnostic framework; Environmental Modelling & Software 2024, 10.1016/j.envsoft.2024.106191)
- Olympus enhanced (Streamlit app for code-free benchmarking; ChemRxiv 2023, 10.26434/chemrxiv-2023-74w8d)
- ProteusAI (Shiny web app for protein engineering; bioRxiv 2024, 10.1101/2024.10.01.616114)
- BORA (LLM-assisted BO research assistant; arXiv 2025, 10.48550/arXiv.2501.16224)
- Atlas (ask/tell brain for self-driving labs; Digital Discovery 2025, 10.1039/d4dd00115j)
