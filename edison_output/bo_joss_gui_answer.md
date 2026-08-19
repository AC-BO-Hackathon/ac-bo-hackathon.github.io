Question: Identify peer-reviewed SOFTWARE papers, especially in the Journal of Open Source Software (JOSS) and also SoftwareX, Digital Discovery, Chemistry-Methods, npj Computational Materials, and Machine Learning: Science and Technology, that present graphical user interfaces, web applications, dashboards, or other low-barrier interfaces for Bayesian optimization or sequential/adaptive design of experiments aimed at experimentalists rather than programmers. For each paper give the tool name, a one-sentence description of the interface and its target audience, and a FULL citation (authors, title, venue, year, DOI). Also note any GUI front ends built on top of established BO libraries such as BoTorch/Ax, scikit-optimize, GPyOpt, Optuna, or BayBE, and whether each tool supports batch experiments, multi-objective optimization, and categorical/mixed variables. Provide a consolidated reference list with DOIs at the end.

# GUI and Web-Based Tools for Bayesian Optimization Aimed at Experimentalists

## Overview

A systematic search of the Journal of Open Source Software (JOSS), Digital Discovery, Machine Learning: Science and Technology (ML:ST), and other peer-reviewed venues identified a growing ecosystem of software tools that present graphical user interfaces (GUIs), web applications, or dashboards for Bayesian optimization (BO) and sequential/adaptive design of experiments. These tools are explicitly designed to lower the barrier for experimentalists who are not expert programmers. The following table consolidates the identified tools and their key features.

| Tool Name | Interface Type | Target Audience | Underlying BO Library | Batch Experiments Support | Multi-Objective Optimization Support | Categorical/Mixed Variables Support | Venue |
|---|---|---|---|---|---|---|---|
| OPTIMEO | Streamlit web app | Experimentalists, researchers, and students without Python knowledge | Ax platform / BoTorch | NR | Yes | Yes | Journal of Open Source Software (bousige2025optimeobayesianoptimization pages 1-2, bousige2025optimeobayesianoptimization pages 2-4) |
| Web-BO | Web GUI | Chemists/researchers without coding experience | BayBE backend with GP models | Yes | No (planned) | Yes | Faraday Discussions (mroz2025webbotowardsincreased pages 7-9, mroz2025webbotowardsincreased pages 5-7, mroz2025webbotowardsincreased pages 9-12, mroz2025webbotowardsincreased pages 1-2, mroz2025webbotowardsincreased pages 2-5) |
| Olympus (enhanced) | Streamlit web app for code-free usage | Chemistry/materials researchers, including limited-programming users | Includes BoTorch/GPyTorch planner among multiple planners | Yes | Yes | Yes | Machine Learning: Science and Technology (original) / ChemRxiv (enhanced) (hickman2023olympusenhancedbenchmarking pages 1-2, hickman2023olympusenhancedbenchmarking pages 7-9, hase2021olympusabenchmarking pages 1-2) |
| BayBE | Python API backend (no standalone GUI) | Experimental planners in chemistry/materials/pharma; backend for GUI tools like Web-BO | In-house BayBE framework with GP + EI | Yes | Yes | Yes | Digital Discovery (fitzner2025baybeabayesian pages 2-3, fitzner2025baybeabayesian pages 1-2, fitzner2025baybeabayesian pages 7-8, fitzner2025baybeabayesian pages 3-4) |
| Atlas | Python ask-tell API (no web GUI) | Self-driving-lab practitioners and experimental scientists | BoTorch / GPyTorch / PyTorch | Yes | Yes | Yes | Digital Discovery (hickman2025atlasabrain pages 18-20, hickman2025atlasabrain pages 4-6, hickman2025atlasabrain pages 3-4, hickman2025atlasabrain pages 6-7, hickman2025atlasabrain pages 9-12) |
| BoFire | Python API; JSON-serializable, REST/API-ready (no GUI described) | Chemical industry practitioners and BO researchers | BoTorch | Yes | Yes | Yes | arXiv (durholt2025bofirebayesianoptimization pages 1-3, durholt2025bofirebayesianoptimization pages 3-6) |
| IvoryOS | Web interface with drag-and-drop workflow design | Self-driving-lab users, including non-programmers | Ax platform integration for BO | NR | NR | NR | Nature Communications (zhang2025ivoryosaninteroperable pages 2-4, zhang2025ivoryosaninteroperable pages 4-5, zhang2025ivoryosaninteroperable pages 1-2, zhang2025ivoryosaninteroperable pages 5-7) |
| ProcessOptimizer | Python ask-tell API (no web GUI) | Experimental scientists and process-optimization professionals | Extended fork/development of scikit-optimize | Yes | Yes | Yes | Journal of Chemical Information and Modeling (bertelsen2025processoptimizeranopensource pages 4-5, bertelsen2025processoptimizeranopensource pages 3-4, bertelsen2025processoptimizeranopensource pages 2-3, bertelsen2025processoptimizeranopensource pages 1-2) |
| ProteusAI | Shiny for Python web app | Protein engineers and experimentalists without computational expertise | In-house BO workflows using surrogate models + EI | NR | NR | Protein-sequence/design variables; mixed-variable support not stated | bioRxiv preprint (funk2024proteusaianopensource pages 16-19, funk2024proteusaianopensource pages 6-8, funk2024proteusaianopensource pages 1-2, funk2024proteusaianopensource pages 2-4, funk2024proteusaianopensource pages 10-11) |
| EDBO / EDBO+ | Web-based GUI | Non-expert chemists | GP-based BO; q-EHVI for multi-objective EDBO | Yes | Yes | Yes (reaction-condition spaces incl. categorical/discrete chemistry variables) | Chimia review / ChemRxiv mention of EDBO+ (hickman2023olympusenhancedbenchmarking pages 7-9, guo2023bayesianoptimizationfor pages 4-5, guo2023bayesianoptimizationfor pages 5-6) |


*Table: This table compares the main low-barrier Bayesian optimization tools identified in the search, emphasizing interface type, audience, backend library, and support for batch, multi-objective, and mixed-variable optimization. It is useful for quickly separating true GUI/web tools from API-first backends that can support experimentalist-facing front ends.*

## Detailed Tool Descriptions

### 1. OPTIMEO (JOSS)

OPTIMEO is a Streamlit-based web application for Bayesian optimization, process tuning, and experimental design (bousige2025optimeobayesianoptimization pages 1-2, bousige2025optimeobayesianoptimization pages 2-4). It is accessible at https://optimeo.streamlit.app/ or can be run locally. The tool targets researchers and students who do not have Python programming knowledge. OPTIMEO is **built on top of the Ax platform and BoTorch**, with additional dependencies including scikit-learn, pyDOE3, dexpy, and doepy for classical design of experiments (bousige2025optimeobayesianoptimization pages 2-4). It supports numerical and categorical variables as well as multi-objective optimization. A notable feature is that it automatically sets editable feature bounds from user-uploaded data and includes built-in DoE generation to help users choose initial experiments (bousige2025optimeobayesianoptimization pages 2-4). The tool is also available as a standalone Python package for integration into robotic high-throughput laboratory workflows (bousige2025optimeobayesianoptimization pages 2-4).

**Citation:** Bousige, C. (2025). OPTIMEO: Bayesian Optimization Web App for Process Tuning, Modeling, and Orchestration. *Journal of Open Source Software*, 10(115), 8510. https://doi.org/10.21105/joss.08510

---

### 2. Web-BO (Faraday Discussions)

Web-BO is a web-based GUI designed to make Bayesian optimization accessible for chemistry applications without requiring coding experience (mroz2025webbotowardsincreased pages 1-2). Users upload datasets in CSV or datalab format, define optimization parameters through interactive web forms, and receive next-experiment recommendations. Web-BO is **built on BayBE** as its BO solver backend and integrates with the datalab electronic laboratory notebook (ELN) (mroz2025webbotowardsincreased pages 7-9, mroz2025webbotowardsincreased pages 5-7). It supports batch experiments (users specify how many experiments to perform per iteration), multiple variable types including integer, continuous, categorical, and chemical (SMILES-based) variables (mroz2025webbotowardsincreased pages 7-9). Currently, Web-BO supports single-objective optimization, with multi-objective and multi-fidelity BO planned for future releases (mroz2025webbotowardsincreased pages 9-12). Future plans also include integration of alternative backends such as BoTorch and BoFire (mroz2025webbotowardsincreased pages 9-12).

**Citation:** Mroz, A. M., Toka, P. N., del Río Chanona, E. A., & Jelfs, K. E. (2025). Web-BO: towards increased accessibility of Bayesian optimisation (BO) for chemistry. *Faraday Discussions*, 256, 221–234. https://doi.org/10.1039/d4fd00109e

---

### 3. Olympus (enhanced) with Streamlit Web Application (ML:ST / ChemRxiv)

Olympus is a benchmarking framework for noisy optimization and experiment planning, originally published in *Machine Learning: Science and Technology* (hase2021olympusabenchmarking pages 1-2). The enhanced version extends the package to support mixed parameter types (continuous, discrete, categorical, ordinal) and multi-objective optimization via achievement scalarizing functions including Weighted Sum, Chebyshev, Chimera, and hypervolume-based strategies (hickman2023olympusenhancedbenchmarking pages 1-2, hickman2023olympusenhancedbenchmarking pages 3-5). Critically, **the enhanced Olympus embeds a Streamlit web application for code-free usage**, enabling researchers to benchmark optimization strategies without writing any code (hickman2023olympusenhancedbenchmarking pages 1-2). The framework includes 23 optimization planners (including BoTorch-based Bayesian optimizers using GPyTorch), 33 benchmark datasets, and supports batched optimization (hickman2023olympusenhancedbenchmarking pages 7-9). Olympus handles mixed continuous-categorical parameter spaces using mixed kernels combining Hamming distance and Matérn 5/2 kernels (hickman2023olympusenhancedbenchmarking pages 7-9).

**Citations:**
- Häse, F., Aldeghi, M., Hickman, R. J., Roch, L. M., Christensen, M., Liles, E., Hein, J. E., & Aspuru-Guzik, A. (2021). Olympus: a benchmarking framework for noisy optimization and experiment planning. *Machine Learning: Science and Technology*, 2, 035021. https://doi.org/10.1088/2632-2153/abedc8
- Hickman, R., Parakh, P., Cheng, A., Ai, Q., Schrier, J., Aldeghi, M., & Aspuru-Guzik, A. (2023). Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. *ChemRxiv*. https://doi.org/10.26434/chemrxiv-2023-74w8d

---

### 4. BayBE (Digital Discovery)

BayBE (Bayesian Back End) is an open-source Python package for experimental planning in the low-to-no-data regime, published in *Digital Discovery* (fitzner2025baybeabayesian pages 2-3, fitzner2025baybeabayesian pages 1-2). While BayBE itself is an API-first library, it is significant as the **underlying BO backend for the Web-BO GUI** (mroz2025webbotowardsincreased pages 7-9). BayBE supports discrete, continuous, and hybrid parameter spaces with chemical and custom categorical encodings (e.g., MORDRED descriptors) that can reduce experimental budgets by at least 50% compared to one-hot encoding (fitzner2025baybeabayesian pages 3-4). It provides multi-objective optimization through desirability scalarization and Pareto-front search, distributed asynchronous workflows supporting partial measurements and multiple experimenters, active learning, transfer learning, and automatic stopping criteria (fitzner2025baybeabayesian pages 2-3, fitzner2025baybeabayesian pages 7-8). BayBE is also used as a backend in NASA benchmarking studies (fitzner2025baybeabayesian pages 2-3).

**Citation:** Fitzner, M., Šošić, A., Hopp, A. V., Müller, M., Rihana, R., Hrovatin, K., Liebig, F., Winkel, M., Halter, W., & Brandenburg, J. G. (2025). BayBE: a Bayesian Back End for experimental planning in the low-to-no-data regime. *Digital Discovery*. https://doi.org/10.1039/d5dd00050e

---

### 5. Atlas (Digital Discovery)

Atlas is a Python library designed as the "brain" for self-driving laboratories, published in *Digital Discovery* (hickman2025atlasabrain pages 1-2, hickman2025atlasabrain pages 2-3). It provides state-of-the-art Bayesian optimization through a high-level ask-tell interface **built on BoTorch, GPyTorch, and PyTorch** (hickman2025atlasabrain pages 4-6, hickman2025atlasabrain pages 2-3). Atlas supports mixed-parameter optimization (continuous, discrete, categorical with vector-valued descriptors), multi-objective optimization via augmented scalarizing functions and hypervolume-based approaches, batch optimization, constrained optimization (known and unknown constraints), robust optimization via the Golem package, multi-fidelity optimization, and meta-learning (hickman2025atlasabrain pages 18-20, hickman2025atlasabrain pages 6-7, hickman2025atlasabrain pages 9-12). Atlas integrates with the Olympus benchmarking framework and ChemOS 2.0 for deployment. While Atlas does not provide a standalone web GUI, it is designed for integration into automated laboratory systems (hickman2025atlasabrain pages 4-6).

**Citation:** Hickman, R. J., Sim, M., Pablo-García, S., Tom, G., Woolhouse, I., Hao, H., Bao, Z., Bannigan, P., Allen, C. J., Aldeghi, M., & Aspuru-Guzik, A. (2025). Atlas: A Brain for Self-driving Laboratories. *Digital Discovery*. https://doi.org/10.1039/d4dd00115j

---

### 6. BoFire (arXiv preprint)

BoFire (Bayesian Optimization Framework Intended for Real Experiments) is an open-source Python package combining BO with design-of-experiments strategies for chemistry optimization (durholt2025bofirebayesianoptimization pages 1-3, durholt2025bofirebayesianoptimization pages 3-6). It is **built on BoTorch** and supports mixed-type variables (continuous, discrete, molecular, categorical), constrained input spaces, and multi-objective optimization through both a priori weighting and a posteriori Pareto-front approximation using qParEGO and q(log)(N)EHVI (durholt2025bofirebayesianoptimization pages 1-3). BoFire supports batch experiments through interpoint equality constraints and is fully JSON-serializable for RESTful API integration, making it suitable for self-driving labs and human-in-the-loop setups (durholt2025bofirebayesianoptimization pages 1-3). While BoFire does not provide a standalone GUI, its JSON-serializability facilitates integration into web dashboards. It has been adopted by multiple chemical companies including BASF and Evonik (durholt2025bofirebayesianoptimization pages 1-3).

**Citation:** Dürholt, J. P., Asche, T. S., Kleinekorte, J., Mancino-Ball, G., Schiller, B., Sung, S., Keupp, J., Osburg, A., Boyne, T., Misener, R., Eldred, R., Costa, W. S., Kappatou, C., Lee, R. M., Linzner, D., Walz, D., Wulkow, N., & Shafei, B. (2025). BoFire: Bayesian Optimization Framework Intended for Real Experiments. *arXiv*, 2408.05040. https://doi.org/10.48550/arxiv.2408.05040

---

### 7. IvoryOS (Nature Communications)

IvoryOS is an open-source orchestrator that automatically generates web interfaces for Python-based self-driving laboratories (zhang2025ivoryosaninteroperable pages 1-2). It provides a **drag-and-drop workflow design interface** where operators visually program experiments by dragging method cards onto a canvas and supports no-code configuration for iterative execution (zhang2025ivoryosaninteroperable pages 2-4, zhang2025ivoryosaninteroperable pages 4-5). For workflows with numerical outputs, IvoryOS **integrates Bayesian optimization via the Ax platform** to enable adaptive exploration and optimization of experimental parameters (zhang2025ivoryosaninteroperable pages 2-4). It also includes text-to-code capabilities using GPT-4 for natural language to executable script translation (zhang2025ivoryosaninteroperable pages 2-4). IvoryOS has been demonstrated across six self-driving laboratories at two institutes (zhang2025ivoryosaninteroperable pages 1-2, zhang2025ivoryosaninteroperable pages 5-7).

**Citation:** Zhang, W., Hao, L., Lai, V., Corkery, R., Jessiman, J., Zhang, J., Liu, J., Sato, Y., Politi, M., Reish, M. E., Greenwood, R., Depner, N., Min, J., El-khawaldeh, R., Prieto, P., Trushina, E., & Hein, J. E. (2025). IvoryOS: an interoperable web interface for orchestrating Python-based self-driving laboratories. *Nature Communications*, 16. https://doi.org/10.1038/s41467-025-60514-w

---

### 8. ProcessOptimizer (Journal of Chemical Information and Modeling)

ProcessOptimizer is an open-source Python package for Bayesian optimization of real-world processes (bertelsen2025processoptimizeranopensource pages 1-2). It is **built as an extended development of scikit-optimize** with numerous new features and default settings tailored for physical process optimization rather than machine learning hyperparameter tuning (bertelsen2025processoptimizeranopensource pages 2-3). It supports continuous, discrete, and categorical variables in combination, batch-mode operation for multiple simultaneous experiment suggestions, and multi-objective Bayesian optimization using NSGA-II for Pareto optimization (bertelsen2025processoptimizeranopensource pages 3-4). The interface uses a Python ask-tell API rather than a web GUI, but it is designed for experimental scientists requiring only minimal Python training (bertelsen2025processoptimizeranopensource pages 4-5, bertelsen2025processoptimizeranopensource pages 1-2).

**Citation:** Bertelsen, S., Carlsen, S., Furbo, S., Nielsen, M. B., Obdrup, A., & Taaning, R. (2025). ProcessOptimizer, an Open-Source Python Package for Easy Optimization of Real-World Processes Using Bayesian Optimization: Showcase of Features and Example of Use. *Journal of Chemical Information and Modeling*, 65, 1702–1707. https://doi.org/10.1021/acs.jcim.4c02240

---

### 9. EDBO / EDBO+ (Web GUI for Chemical Reaction Optimization)

EDBO (Experimental Design via Bayesian Optimization) and its successor EDBO+ provide a **web-based graphical user interface** aimed at equipping any chemist with a BO tool for reaction optimization (guo2023bayesianoptimizationfor pages 4-5, hickman2023olympusenhancedbenchmarking pages 7-9). EDBO was developed by Shields, Doyle, and colleagues and demonstrated efficient optimization of Buchwald–Hartwig, Suzuki–Miyaura, Mitsunobu, and deoxyfluorination reactions, finding optimal conditions within 30–50 experiments from design spaces of hundreds of thousands of combinations (guo2023bayesianoptimizationfor pages 4-5). EDBO+ extends the platform to multi-objective optimization of chemical reactions using GP surrogates with q-Expected HyperVolume Improvement (q-EHVI) acquisition, enabling simultaneous optimization of yield and enantioselectivity (guo2023bayesianoptimizationfor pages 5-6). EDBO+ is described as featuring a web-based GUI democratizing the software for non-experts (hickman2023olympusenhancedbenchmarking pages 7-9). The tool supports categorical reaction variables (solvents, ligands, bases) and batch acquisition strategies including Kriging Believer and PDTS (guo2023bayesianoptimizationfor pages 4-5, guo2023bayesianoptimizationfor pages 5-6).

**Citations (as referenced in reviews):**
- Shields, B. J., Stevens, J., Li, J., Parasram, M., Damani, F., Alvarado, J. I. M., Janey, J. M., Adams, R. P., & Doyle, A. G. (2021). Bayesian reaction optimization as a tool for chemical synthesis. *Nature*, 590, 89–96. https://doi.org/10.1038/s41586-021-03213-y
- Torres, J. A. G., Lau, S. H., Anchuri, P., Stevens, J. M., Tabora, J. E., Li, J., Borovika, A., Adams, R. P., & Doyle, A. G. (2022). A multi-objective active learning platform and web app for reaction optimization. *Journal of the American Chemical Society*, 144, 19999–20007. https://doi.org/10.1021/jacs.2c08592

---

### 10. ProteusAI (bioRxiv preprint)

ProteusAI is an open-source platform for machine-learning-guided protein design and engineering, accessible as a **web application built on Shiny for Python** (deployed on Microsoft Azure) and as a Python package (funk2024proteusaianopensource pages 16-19, funk2024proteusaianopensource pages 1-2, funk2024proteusaianopensource pages 2-4). The platform uses Bayesian optimization with Expected Improvement acquisition functions and surrogate models (Random Forest and Gaussian Processes) to iteratively optimize protein properties such as catalytic activity, binding affinity, and thermostability (funk2024proteusaianopensource pages 6-8, funk2024proteusaianopensource pages 10-11). It targets experimentalists who lack computational expertise and supports multiple protein sequence representations including ESM-2 protein language models and BLOSUM encodings (funk2024proteusaianopensource pages 6-8, funk2024proteusaianopensource pages 2-4). Note that ProteusAI is currently a preprint and has not yet appeared in a peer-reviewed journal.

**Citation:** Funk, J., Machado, L., Bradley, S. A., Napiorkowska, M., Gallegos-Dextre, R., Pashkova, L., Madsen, N. G., Webel, H., Phaneuf, P. V., Jenkins, T. P., & Acevedo-Rocha, C. G. (2024). ProteusAI: An Open-Source and User-Friendly Platform for Machine Learning-Guided Protein Design and Engineering. *bioRxiv*. https://doi.org/10.1101/2024.10.01.616114

---

## GUI Front Ends Built on Established BO Libraries

Several of the identified tools are explicitly built on top of well-known BO libraries:

- **OPTIMEO** is built on **Ax/BoTorch** (bousige2025optimeobayesianoptimization pages 1-2, bousige2025optimeobayesianoptimization pages 2-4).
- **Web-BO** uses **BayBE** as its solver backend (mroz2025webbotowardsincreased pages 7-9, mroz2025webbotowardsincreased pages 5-7).
- **IvoryOS** integrates BO via the **Ax platform** (zhang2025ivoryosaninteroperable pages 2-4, zhang2025ivoryosaninteroperable pages 4-5).
- **Atlas** and **BoFire** are both built on **BoTorch/GPyTorch** (hickman2025atlasabrain pages 4-6, durholt2025bofirebayesianoptimization pages 1-3).
- **ProcessOptimizer** is an extended fork/development of **scikit-optimize** (bertelsen2025processoptimizeranopensource pages 2-3).
- **Olympus (enhanced)** includes a BoTorch-based planner among its 23 optimization planners (hickman2023olympusenhancedbenchmarking pages 7-9).

Additional tools mentioned in the OPTIMEO paper include **BOXVIA** (a Bayesian optimization executable and visualizable application), **MADGUI** (Multi-Application Design Graphical User Interface for active learning assisted by BO), and **Sycofinder** (a web-based UI for MOF synthesis optimization) (bousige2025optimeobayesianoptimization pages 2-4, bousige2025optimeobayesianoptimization pages 1-2); however, full text for these papers could not be retrieved during this search.

---

## Consolidated Reference List

1. Bousige, C. (2025). OPTIMEO: Bayesian Optimization Web App for Process Tuning, Modeling, and Orchestration. *Journal of Open Source Software*, 10(115), 8510. https://doi.org/10.21105/joss.08510

2. Mroz, A. M., Toka, P. N., del Río Chanona, E. A., & Jelfs, K. E. (2025). Web-BO: towards increased accessibility of Bayesian optimisation (BO) for chemistry. *Faraday Discussions*, 256, 221–234. https://doi.org/10.1039/d4fd00109e

3. Häse, F., Aldeghi, M., Hickman, R. J., Roch, L. M., Christensen, M., Liles, E., Hein, J. E., & Aspuru-Guzik, A. (2021). Olympus: a benchmarking framework for noisy optimization and experiment planning. *Machine Learning: Science and Technology*, 2, 035021. https://doi.org/10.1088/2632-2153/abedc8

4. Hickman, R., Parakh, P., Cheng, A., Ai, Q., Schrier, J., Aldeghi, M., & Aspuru-Guzik, A. (2023). Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. *ChemRxiv*. https://doi.org/10.26434/chemrxiv-2023-74w8d

5. Fitzner, M., Šošić, A., Hopp, A. V., Müller, M., Rihana, R., Hrovatin, K., Liebig, F., Winkel, M., Halter, W., & Brandenburg, J. G. (2025). BayBE: a Bayesian Back End for experimental planning in the low-to-no-data regime. *Digital Discovery*. https://doi.org/10.1039/d5dd00050e

6. Hickman, R. J., Sim, M., Pablo-García, S., Tom, G., Woolhouse, I., Hao, H., Bao, Z., Bannigan, P., Allen, C. J., Aldeghi, M., & Aspuru-Guzik, A. (2025). Atlas: A Brain for Self-driving Laboratories. *Digital Discovery*. https://doi.org/10.1039/d4dd00115j

7. Dürholt, J. P., Asche, T. S., Kleinekorte, J., Mancino-Ball, G., Schiller, B., Sung, S., Keupp, J., Osburg, A., Boyne, T., Misener, R., Eldred, R., Costa, W. S., Kappatou, C., Lee, R. M., Linzner, D., Walz, D., Wulkow, N., & Shafei, B. (2025). BoFire: Bayesian Optimization Framework Intended for Real Experiments. *arXiv*, 2408.05040. https://doi.org/10.48550/arxiv.2408.05040

8. Zhang, W., Hao, L., Lai, V., Corkery, R., Jessiman, J., Zhang, J., Liu, J., Sato, Y., Politi, M., Reish, M. E., Greenwood, R., Depner, N., Min, J., El-khawaldeh, R., Prieto, P., Trushina, E., & Hein, J. E. (2025). IvoryOS: an interoperable web interface for orchestrating Python-based self-driving laboratories. *Nature Communications*, 16. https://doi.org/10.1038/s41467-025-60514-w

9. Bertelsen, S., Carlsen, S., Furbo, S., Nielsen, M. B., Obdrup, A., & Taaning, R. (2025). ProcessOptimizer, an Open-Source Python Package for Easy Optimization of Real-World Processes Using Bayesian Optimization: Showcase of Features and Example of Use. *Journal of Chemical Information and Modeling*, 65, 1702–1707. https://doi.org/10.1021/acs.jcim.4c02240

10. Shields, B. J., Stevens, J., Li, J., Parasram, M., Damani, F., Alvarado, J. I. M., Janey, J. M., Adams, R. P., & Doyle, A. G. (2021). Bayesian reaction optimization as a tool for chemical synthesis. *Nature*, 590, 89–96. https://doi.org/10.1038/s41586-021-03213-y

11. Torres, J. A. G., Lau, S. H., Anchuri, P., Stevens, J. M., Tabora, J. E., Li, J., Borovika, A., Adams, R. P., & Doyle, A. G. (2022). A multi-objective active learning platform and web app for reaction optimization. *Journal of the American Chemical Society*, 144, 19999–20007. https://doi.org/10.1021/jacs.2c08592

12. Funk, J., Machado, L., Bradley, S. A., Napiorkowska, M., Gallegos-Dextre, R., Pashkova, L., Madsen, N. G., Webel, H., Phaneuf, P. V., Jenkins, T. P., & Acevedo-Rocha, C. G. (2024). ProteusAI: An Open-Source and User-Friendly Platform for Machine Learning-Guided Protein Design and Engineering. *bioRxiv*. https://doi.org/10.1101/2024.10.01.616114

13. Guo, J., Ranković, B., & Schwaller, P. (2023). Bayesian Optimization for Chemical Reactions. *Chimia*, 77(1/2), 31–38. https://doi.org/10.2533/chimia.2023.31

References

1. (bousige2025optimeobayesianoptimization pages 1-2): Colin Bousige. Optimeo: bayesian optimization web app for process tuning, modeling, and orchestration. Journal of Open Source Software, 10:8510, Nov 2025. URL: https://doi.org/10.21105/joss.08510, doi:10.21105/joss.08510. This article has 0 citations and is from a peer-reviewed journal.

2. (bousige2025optimeobayesianoptimization pages 2-4): Colin Bousige. Optimeo: bayesian optimization web app for process tuning, modeling, and orchestration. Journal of Open Source Software, 10:8510, Nov 2025. URL: https://doi.org/10.21105/joss.08510, doi:10.21105/joss.08510. This article has 0 citations and is from a peer-reviewed journal.

3. (mroz2025webbotowardsincreased pages 7-9): Austin M. Mroz, Piotr N. Toka, Ehecatl Antonio del Río Chanona, and Kim E. Jelfs. Web-bo: towards increased accessibility of bayesian optimisation (bo) for chemistry. Faraday Discussions, 256:221-234, Jan 2025. URL: https://doi.org/10.1039/d4fd00109e, doi:10.1039/d4fd00109e. This article has 7 citations and is from a peer-reviewed journal.

4. (mroz2025webbotowardsincreased pages 5-7): Austin M. Mroz, Piotr N. Toka, Ehecatl Antonio del Río Chanona, and Kim E. Jelfs. Web-bo: towards increased accessibility of bayesian optimisation (bo) for chemistry. Faraday Discussions, 256:221-234, Jan 2025. URL: https://doi.org/10.1039/d4fd00109e, doi:10.1039/d4fd00109e. This article has 7 citations and is from a peer-reviewed journal.

5. (mroz2025webbotowardsincreased pages 9-12): Austin M. Mroz, Piotr N. Toka, Ehecatl Antonio del Río Chanona, and Kim E. Jelfs. Web-bo: towards increased accessibility of bayesian optimisation (bo) for chemistry. Faraday Discussions, 256:221-234, Jan 2025. URL: https://doi.org/10.1039/d4fd00109e, doi:10.1039/d4fd00109e. This article has 7 citations and is from a peer-reviewed journal.

6. (mroz2025webbotowardsincreased pages 1-2): Austin M. Mroz, Piotr N. Toka, Ehecatl Antonio del Río Chanona, and Kim E. Jelfs. Web-bo: towards increased accessibility of bayesian optimisation (bo) for chemistry. Faraday Discussions, 256:221-234, Jan 2025. URL: https://doi.org/10.1039/d4fd00109e, doi:10.1039/d4fd00109e. This article has 7 citations and is from a peer-reviewed journal.

7. (mroz2025webbotowardsincreased pages 2-5): Austin M. Mroz, Piotr N. Toka, Ehecatl Antonio del Río Chanona, and Kim E. Jelfs. Web-bo: towards increased accessibility of bayesian optimisation (bo) for chemistry. Faraday Discussions, 256:221-234, Jan 2025. URL: https://doi.org/10.1039/d4fd00109e, doi:10.1039/d4fd00109e. This article has 7 citations and is from a peer-reviewed journal.

8. (hickman2023olympusenhancedbenchmarking pages 1-2): Riley Hickman, Priyansh Parakh, Austin Cheng, Qianxiang Ai, Joshua Schrier, Matteo Aldeghi, and Alán Aspuru-Guzik. Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. ChemRxiv, May 2023. URL: https://doi.org/10.26434/chemrxiv-2023-74w8d, doi:10.26434/chemrxiv-2023-74w8d. This article has 13 citations.

9. (hickman2023olympusenhancedbenchmarking pages 7-9): Riley Hickman, Priyansh Parakh, Austin Cheng, Qianxiang Ai, Joshua Schrier, Matteo Aldeghi, and Alán Aspuru-Guzik. Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. ChemRxiv, May 2023. URL: https://doi.org/10.26434/chemrxiv-2023-74w8d, doi:10.26434/chemrxiv-2023-74w8d. This article has 13 citations.

10. (hase2021olympusabenchmarking pages 1-2): Florian Häse, Matteo Aldeghi, Riley J Hickman, Loïc M Roch, Melodie Christensen, Elena Liles, Jason E Hein, and Alán Aspuru-Guzik. Olympus: a benchmarking framework for noisy optimization and experiment planning. Machine Learning: Science and Technology, 2:035021, Jul 2021. URL: https://doi.org/10.1088/2632-2153/abedc8, doi:10.1088/2632-2153/abedc8. This article has 140 citations and is from a peer-reviewed journal.

11. (fitzner2025baybeabayesian pages 2-3): Martin Fitzner, Adrian Šošić, Alexander V. Hopp, Marcel Müller, Rim Rihana, Karin Hrovatin, Fabian Liebig, Mathias Winkel, Wolfgang Halter, and Jan Gerit Brandenburg. Baybe: a bayesian back end for experimental planning in the low-to-no-data regime. Digital Discovery, Jan 2025. URL: https://doi.org/10.1039/d5dd00050e, doi:10.1039/d5dd00050e. This article has 34 citations and is from a peer-reviewed journal.

12. (fitzner2025baybeabayesian pages 1-2): Martin Fitzner, Adrian Šošić, Alexander V. Hopp, Marcel Müller, Rim Rihana, Karin Hrovatin, Fabian Liebig, Mathias Winkel, Wolfgang Halter, and Jan Gerit Brandenburg. Baybe: a bayesian back end for experimental planning in the low-to-no-data regime. Digital Discovery, Jan 2025. URL: https://doi.org/10.1039/d5dd00050e, doi:10.1039/d5dd00050e. This article has 34 citations and is from a peer-reviewed journal.

13. (fitzner2025baybeabayesian pages 7-8): Martin Fitzner, Adrian Šošić, Alexander V. Hopp, Marcel Müller, Rim Rihana, Karin Hrovatin, Fabian Liebig, Mathias Winkel, Wolfgang Halter, and Jan Gerit Brandenburg. Baybe: a bayesian back end for experimental planning in the low-to-no-data regime. Digital Discovery, Jan 2025. URL: https://doi.org/10.1039/d5dd00050e, doi:10.1039/d5dd00050e. This article has 34 citations and is from a peer-reviewed journal.

14. (fitzner2025baybeabayesian pages 3-4): Martin Fitzner, Adrian Šošić, Alexander V. Hopp, Marcel Müller, Rim Rihana, Karin Hrovatin, Fabian Liebig, Mathias Winkel, Wolfgang Halter, and Jan Gerit Brandenburg. Baybe: a bayesian back end for experimental planning in the low-to-no-data regime. Digital Discovery, Jan 2025. URL: https://doi.org/10.1039/d5dd00050e, doi:10.1039/d5dd00050e. This article has 34 citations and is from a peer-reviewed journal.

15. (hickman2025atlasabrain pages 18-20): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

16. (hickman2025atlasabrain pages 4-6): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

17. (hickman2025atlasabrain pages 3-4): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

18. (hickman2025atlasabrain pages 6-7): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

19. (hickman2025atlasabrain pages 9-12): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

20. (durholt2025bofirebayesianoptimization pages 1-3): Johannes P. Dürholt, Thomas S. Asche, Johanna Kleinekorte, Gabriel Mancino-Ball, Benjamin Schiller, Simon Sung, Julian Keupp, Aaron Osburg, Toby Boyne, Ruth Misener, Rosona Eldred, Wagner Steuer Costa, Chrysoula Kappatou, Robert M. Lee, Dominik Linzner, David Walz, Niklas Wulkow, and Behrang Shafei. Bofire: bayesian optimization framework intended for real experiments. ArXiv, Aug 2025. URL: https://doi.org/10.48550/arxiv.2408.05040, doi:10.48550/arxiv.2408.05040. This article has 20 citations.

21. (durholt2025bofirebayesianoptimization pages 3-6): Johannes P. Dürholt, Thomas S. Asche, Johanna Kleinekorte, Gabriel Mancino-Ball, Benjamin Schiller, Simon Sung, Julian Keupp, Aaron Osburg, Toby Boyne, Ruth Misener, Rosona Eldred, Wagner Steuer Costa, Chrysoula Kappatou, Robert M. Lee, Dominik Linzner, David Walz, Niklas Wulkow, and Behrang Shafei. Bofire: bayesian optimization framework intended for real experiments. ArXiv, Aug 2025. URL: https://doi.org/10.48550/arxiv.2408.05040, doi:10.48550/arxiv.2408.05040. This article has 20 citations.

22. (zhang2025ivoryosaninteroperable pages 2-4): Wenyu Zhang, Lucy Hao, Veronica Lai, Ryan Corkery, Jacob Jessiman, Jiayu Zhang, Junliang Liu, Yusuke Sato, Maria Politi, Matthew E. Reish, Rebekah Greenwood, Noah Depner, Jiyoon Min, Rama El-khawaldeh, Paloma Prieto, Ekaterina Trushina, and Jason E. Hein. Ivoryos: an interoperable web interface for orchestrating python-based self-driving laboratories. Nature Communications, Jun 2025. URL: https://doi.org/10.1038/s41467-025-60514-w, doi:10.1038/s41467-025-60514-w. This article has 30 citations and is from a highest quality peer-reviewed journal.

23. (zhang2025ivoryosaninteroperable pages 4-5): Wenyu Zhang, Lucy Hao, Veronica Lai, Ryan Corkery, Jacob Jessiman, Jiayu Zhang, Junliang Liu, Yusuke Sato, Maria Politi, Matthew E. Reish, Rebekah Greenwood, Noah Depner, Jiyoon Min, Rama El-khawaldeh, Paloma Prieto, Ekaterina Trushina, and Jason E. Hein. Ivoryos: an interoperable web interface for orchestrating python-based self-driving laboratories. Nature Communications, Jun 2025. URL: https://doi.org/10.1038/s41467-025-60514-w, doi:10.1038/s41467-025-60514-w. This article has 30 citations and is from a highest quality peer-reviewed journal.

24. (zhang2025ivoryosaninteroperable pages 1-2): Wenyu Zhang, Lucy Hao, Veronica Lai, Ryan Corkery, Jacob Jessiman, Jiayu Zhang, Junliang Liu, Yusuke Sato, Maria Politi, Matthew E. Reish, Rebekah Greenwood, Noah Depner, Jiyoon Min, Rama El-khawaldeh, Paloma Prieto, Ekaterina Trushina, and Jason E. Hein. Ivoryos: an interoperable web interface for orchestrating python-based self-driving laboratories. Nature Communications, Jun 2025. URL: https://doi.org/10.1038/s41467-025-60514-w, doi:10.1038/s41467-025-60514-w. This article has 30 citations and is from a highest quality peer-reviewed journal.

25. (zhang2025ivoryosaninteroperable pages 5-7): Wenyu Zhang, Lucy Hao, Veronica Lai, Ryan Corkery, Jacob Jessiman, Jiayu Zhang, Junliang Liu, Yusuke Sato, Maria Politi, Matthew E. Reish, Rebekah Greenwood, Noah Depner, Jiyoon Min, Rama El-khawaldeh, Paloma Prieto, Ekaterina Trushina, and Jason E. Hein. Ivoryos: an interoperable web interface for orchestrating python-based self-driving laboratories. Nature Communications, Jun 2025. URL: https://doi.org/10.1038/s41467-025-60514-w, doi:10.1038/s41467-025-60514-w. This article has 30 citations and is from a highest quality peer-reviewed journal.

26. (bertelsen2025processoptimizeranopensource pages 4-5): Søren Bertelsen, Sigurd Carlsen, Søren Furbo, Morten Bormann Nielsen, Aksel Obdrup, and Rolf Taaning. Processoptimizer, an open-source python package for easy optimization of real-world processes using bayesian optimization: showcase of features and example of use. Journal of Chemical Information and Modeling, 65:1702-1707, Feb 2025. URL: https://doi.org/10.1021/acs.jcim.4c02240, doi:10.1021/acs.jcim.4c02240. This article has 11 citations and is from a peer-reviewed journal.

27. (bertelsen2025processoptimizeranopensource pages 3-4): Søren Bertelsen, Sigurd Carlsen, Søren Furbo, Morten Bormann Nielsen, Aksel Obdrup, and Rolf Taaning. Processoptimizer, an open-source python package for easy optimization of real-world processes using bayesian optimization: showcase of features and example of use. Journal of Chemical Information and Modeling, 65:1702-1707, Feb 2025. URL: https://doi.org/10.1021/acs.jcim.4c02240, doi:10.1021/acs.jcim.4c02240. This article has 11 citations and is from a peer-reviewed journal.

28. (bertelsen2025processoptimizeranopensource pages 2-3): Søren Bertelsen, Sigurd Carlsen, Søren Furbo, Morten Bormann Nielsen, Aksel Obdrup, and Rolf Taaning. Processoptimizer, an open-source python package for easy optimization of real-world processes using bayesian optimization: showcase of features and example of use. Journal of Chemical Information and Modeling, 65:1702-1707, Feb 2025. URL: https://doi.org/10.1021/acs.jcim.4c02240, doi:10.1021/acs.jcim.4c02240. This article has 11 citations and is from a peer-reviewed journal.

29. (bertelsen2025processoptimizeranopensource pages 1-2): Søren Bertelsen, Sigurd Carlsen, Søren Furbo, Morten Bormann Nielsen, Aksel Obdrup, and Rolf Taaning. Processoptimizer, an open-source python package for easy optimization of real-world processes using bayesian optimization: showcase of features and example of use. Journal of Chemical Information and Modeling, 65:1702-1707, Feb 2025. URL: https://doi.org/10.1021/acs.jcim.4c02240, doi:10.1021/acs.jcim.4c02240. This article has 11 citations and is from a peer-reviewed journal.

30. (funk2024proteusaianopensource pages 16-19): Jonathan Funk, Laura Machado, Samuel A. Bradley, Marta Napiorkowska, Rodrigo Gallegos-Dextre, Liubov Pashkova, Niklas G. Madsen, Henry Webel, Patrick V. Phaneuf, Timothy P. Jenkins, and Carlos G. Acevedo-Rocha. Proteusai: an open-source and user-friendly platform for machine learning-guided protein design and engineering. bioRxiv, Oct 2024. URL: https://doi.org/10.1101/2024.10.01.616114, doi:10.1101/2024.10.01.616114. This article has 8 citations.

31. (funk2024proteusaianopensource pages 6-8): Jonathan Funk, Laura Machado, Samuel A. Bradley, Marta Napiorkowska, Rodrigo Gallegos-Dextre, Liubov Pashkova, Niklas G. Madsen, Henry Webel, Patrick V. Phaneuf, Timothy P. Jenkins, and Carlos G. Acevedo-Rocha. Proteusai: an open-source and user-friendly platform for machine learning-guided protein design and engineering. bioRxiv, Oct 2024. URL: https://doi.org/10.1101/2024.10.01.616114, doi:10.1101/2024.10.01.616114. This article has 8 citations.

32. (funk2024proteusaianopensource pages 1-2): Jonathan Funk, Laura Machado, Samuel A. Bradley, Marta Napiorkowska, Rodrigo Gallegos-Dextre, Liubov Pashkova, Niklas G. Madsen, Henry Webel, Patrick V. Phaneuf, Timothy P. Jenkins, and Carlos G. Acevedo-Rocha. Proteusai: an open-source and user-friendly platform for machine learning-guided protein design and engineering. bioRxiv, Oct 2024. URL: https://doi.org/10.1101/2024.10.01.616114, doi:10.1101/2024.10.01.616114. This article has 8 citations.

33. (funk2024proteusaianopensource pages 2-4): Jonathan Funk, Laura Machado, Samuel A. Bradley, Marta Napiorkowska, Rodrigo Gallegos-Dextre, Liubov Pashkova, Niklas G. Madsen, Henry Webel, Patrick V. Phaneuf, Timothy P. Jenkins, and Carlos G. Acevedo-Rocha. Proteusai: an open-source and user-friendly platform for machine learning-guided protein design and engineering. bioRxiv, Oct 2024. URL: https://doi.org/10.1101/2024.10.01.616114, doi:10.1101/2024.10.01.616114. This article has 8 citations.

34. (funk2024proteusaianopensource pages 10-11): Jonathan Funk, Laura Machado, Samuel A. Bradley, Marta Napiorkowska, Rodrigo Gallegos-Dextre, Liubov Pashkova, Niklas G. Madsen, Henry Webel, Patrick V. Phaneuf, Timothy P. Jenkins, and Carlos G. Acevedo-Rocha. Proteusai: an open-source and user-friendly platform for machine learning-guided protein design and engineering. bioRxiv, Oct 2024. URL: https://doi.org/10.1101/2024.10.01.616114, doi:10.1101/2024.10.01.616114. This article has 8 citations.

35. (guo2023bayesianoptimizationfor pages 4-5): Jeff Guo, Bojana Ranković, and Philippe Schwaller. Bayesian optimization for chemical reactions. Chimia, 77 1-2:31-38, Feb 2023. URL: https://doi.org/10.2533/chimia.2023.31, doi:10.2533/chimia.2023.31. This article has 92 citations and is from a peer-reviewed journal.

36. (guo2023bayesianoptimizationfor pages 5-6): Jeff Guo, Bojana Ranković, and Philippe Schwaller. Bayesian optimization for chemical reactions. Chimia, 77 1-2:31-38, Feb 2023. URL: https://doi.org/10.2533/chimia.2023.31, doi:10.2533/chimia.2023.31. This article has 92 citations and is from a peer-reviewed journal.

37. (hickman2023olympusenhancedbenchmarking pages 3-5): Riley Hickman, Priyansh Parakh, Austin Cheng, Qianxiang Ai, Joshua Schrier, Matteo Aldeghi, and Alán Aspuru-Guzik. Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. ChemRxiv, May 2023. URL: https://doi.org/10.26434/chemrxiv-2023-74w8d, doi:10.26434/chemrxiv-2023-74w8d. This article has 13 citations.

38. (hickman2025atlasabrain pages 1-2): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.

39. (hickman2025atlasabrain pages 2-3): Riley J. Hickman, Malcolm Sim, Sergio Pablo-García, Gary Tom, Ivan Woolhouse, Han Hao, Zeqing Bao, Pauric Bannigan, C. J. Allen, Matteo Aldeghi, and Alán Aspuru-Guzik. Atlas: a brain for self-driving laboratories. Digital Discovery, Sep 2025. URL: https://doi.org/10.1039/d4dd00115j, doi:10.1039/d4dd00115j. This article has 70 citations and is from a peer-reviewed journal.