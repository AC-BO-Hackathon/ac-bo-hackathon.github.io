Question: Survey of open-source SOFTWARE REPOSITORIES (GitHub or similar) at the intersection of large language models (LLMs) and Bayesian optimization (BO) for chemistry, materials discovery, and experimental design, from 2023-2026. For each tool or framework give: the repository name and URL, a one-sentence description of how it combines or compares LLMs and BO, and the associated paper with a FULL citation (authors, title, venue, year, DOI) when one exists. Include, where relevant: hybrid LLM+BO optimizers (e.g., BORA), LLM agents that orchestrate BO libraries such as BoTorch/Ax or BayBE, LLM-based surrogate or in-context regression tools, benchmark suites that pit LLMs against BO on optimization tasks, and LLM copilots for self-driving laboratories. Provide a consolidated list at the end.

# Open-source LLM–Bayesian-optimization software, 2023–2026

## Scope and evidence standard

This survey includes repositories whose software either (i) combines an LLM with a statistical BO loop, (ii) uses an LLM or language-model representation as the BO surrogate, prior, or proposal mechanism, (iii) lets an LLM agent invoke BO tools, (iv) benchmarks LLM optimization against BO, or (v) supplies an LLM-facing experimental-design/self-driving-laboratory interface with an explicit BO comparison. I distinguish **verified repository links**—links stated in the retrieved primary literature—from **relevant projects whose exact repository URL was not recoverable**, rather than guessing URLs.

| Repository / framework | URL | Category / domain | One-sentence LLM+BO relationship | Associated paper short citation and DOI |
|---|---|---|---|---|
| LLM4BO | https://github.com/learningmatter-mit/LLM4BO | Hybrid/benchmark suite for biochemical discovery, molecular optimization, protein design | Compares off-the-shelf, fine-tuned, and agentic LLM approaches against statistical BO and includes an agentic workflow that orchestrates BO-style search for chemistry/biology tasks. (akke2025bayesianoptimizationfor pages 10-12) | Akke et al., *Bayesian Optimization for Biochemical Discovery with LLMs*, ChemRxiv, 2025, DOI: 10.26434/chemrxiv-2025-w1wsh. (akke2025bayesianoptimizationfor pages 10-12) |
| LLINBO | https://github.com/UMDataScienceLab/LLM-in-the-Loop-BO | Hybrid LLM+BO; trustworthy BO with engineering proof-of-concept | Uses LLM reasoning mainly for early exploration while a statistical surrogate expert such as a GP handles principled exploitation in BO. (chang2025llinbotrustworthyllmintheloop pages 21-23) | Chang et al., *LLINBO: Trustworthy LLM-in-the-Loop Bayesian Optimization*, arXiv, 2025, DOI: 10.48550/arXiv.2505.14756. (chang2025llinbotrustworthyllmintheloop pages 21-23) |
| OptFormer / Embed-then-Regress | https://github.com/google-research/optformer/tree/main/optformer/embed_then_regress | LLM-based surrogate / in-context regression for general BO over string inputs | Recasts BO inputs as strings and uses pretrained language-model embeddings plus regression to perform BO across synthetic, combinatorial, and HPO tasks. (nguyen2024predictingfromstrings pages 16-17) | Nguyen et al., *Predicting from Strings: Language Model Embeddings for Bayesian Optimization*, arXiv, 2024, DOI: 10.48550/arXiv.2410.10190. (nguyen2024predictingfromstrings pages 16-17) |
| Coscientist | https://github.com/gomesgroup/coscientist | LLM copilot / self-driving lab for chemistry | An LLM agent plans and executes chemistry experiments and was explicitly compared against standard Bayesian optimization on reaction-optimization tasks. (boiko2023autonomouschemicalresearch pages 10-13) | Boiko, MacKnight, Kline, Gomes, *Autonomous Chemical Research with Large Language Models*, Nature, 2023, DOI: 10.1038/s41586-023-06792-0. (boiko2023autonomouschemicalresearch pages 10-13) |
| BORA | Repository URL not recovered from retrieved text | Hybrid LLM+BO assistant for scientific optimization | Couples LLM-generated domain-knowledge suggestions and commentary with BO to escape local minima and contextualize optimization in scientific tasks. (cisse2025languagebasedbayesianoptimization pages 1-2, cisse2025languagebasedbayesianoptimization pages 24-25) | Cissé et al., *Language-Based Bayesian Optimization Research Assistant (BORA)*, arXiv, 2025, DOI: 10.48550/arXiv.2501.16224. (cisse2025languagebasedbayesianoptimization pages 1-2) |


*Table: This table summarizes the most strongly verified open-source repositories at the intersection of LLMs and Bayesian optimization from 2023-2026, using only URLs explicitly recovered in the conversation. It highlights the minimum required tools plus BORA, whose repository URL was not recoverable from the retrieved primary text, so no link is invented.*

## 1. Hybrid LLM + statistical BO

### BORA — Language-Based Bayesian Optimization Research Assistant

- **Repository:** BORA; the paper states that source code is available, but the complete GitHub URL was truncated in the retrieved primary text, so an exact URL cannot be responsibly supplied here.
- **LLM–BO relationship:** BORA dynamically blends conventional BO proposals with LLM-generated hypotheses intended to redirect searches from unproductive local regions; it also validates LLM suggestions, falls back to vanilla BO when suggestions are invalid, and generates human-readable commentary and final experimental recommendations. (cisse2025languagebasedbayesianoptimization pages 1-2, cisse2025languagebasedbayesianoptimization pages 24-25)
- **Applications:** Synthetic functions up to 15 variables and scientific examples involving chemical-materials design, solar-energy production, crop production, and a pétanque model. (cisse2025languagebasedbayesianoptimization pages 1-2)
- **Paper:** Abdoulatif Cissé, Xenophon Evangelopoulos, Vladimir V. Gusev, and Andrew I. Cooper, “Language-Based Bayesian Optimization Research Assistant (BORA),” *arXiv*, 2025. DOI: **10.48550/arXiv.2501.16224**. (cisse2025languagebasedbayesianoptimization pages 1-2)

### LLM4BO — Bayesian Optimization for Biochemical Discovery with LLMs

- **Repository:** **LLM4BO**, https://github.com/learningmatter-mit/LLM4BO — code and data are released under the MIT License. (akke2025bayesianoptimizationfor pages 10-12)
- **LLM–BO relationship:** The repository compares off-the-shelf, fine-tuned, and agentic LLM optimizers with statistical BO on molecular and protein-design tasks; its agentic workflow gives the LLM chemical/filtering tools and a statistical BO tool, while fine-tuned models learn BO-like behavior from synthetic optimization trajectories. (akke2025bayesianoptimizationfor pages 2-3, akke2025bayesianoptimizationfor pages 10-12)
- **Paper:** Mattias Akke, Soojung Yang, Jurgis Ruza, Jinyeop Song, Elton Pan, and Rafael Gómez-Bombarelli, “Bayesian Optimization for Biochemical Discovery with LLMs,” *ChemRxiv*, 2025. DOI: **10.26434/chemrxiv-2025-w1wsh**. (akke2025bayesianoptimizationfor pages 10-12)

### LLINBO — LLM-in-the-Loop Bayesian Optimization

- **Repository:** **LLM-in-the-Loop-BO**, https://github.com/UMDataScienceLab/LLM-in-the-Loop-BO.
- **LLM–BO relationship:** LLINBO is a hybrid optimizer that uses contextual LLM reasoning primarily for early exploration and transfers control toward a calibrated statistical surrogate, such as a Gaussian process, for reliable exploitation; the paper also evaluates LLAMBO/LLAMBO-light prompts in a physical 3D-printing optimization proof-of-concept. (chang2025llinbotrustworthyllmintheloop pages 21-23)
- **Paper:** Chih-Yu Chang, Milad Azvar, Chinedum Okwudire, and Raed Kontar, “LLINBO: Trustworthy LLM-in-the-Loop Bayesian Optimization,” *arXiv*, 2025. DOI: **10.48550/arXiv.2505.14756**.

### GOLLuM — Gaussian Process Optimized LLMs

- **Repository:** GOLLuM; an exact public repository URL was not present in the retrieved primary text.
- **LLM–BO relationship:** GOLLuM makes an LLM representation the learned deep kernel of a GP BO surrogate, jointly optimizing LoRA/projection parameters and GP marginal likelihood to obtain chemically informative features with predictive uncertainty; it was tested across 19 chemistry benchmarks, including Buchwald–Hartwig reaction optimization. (rankovic2504gollumgaussianprocess pages 2-4, rankovic2504gollumgaussianprocess pages 37-38)
- **Paper:** Bojana Ranković and Philippe Schwaller, “GOLLuM: Gaussian Process Optimized LLMs—Reframing LLM Finetuning through Bayesian Optimization,” *arXiv*, 2025. DOI: **10.48550/arXiv.2504.06265**. (rankovic2504gollumgaussianprocess pages 2-4)

## 2. LLM-based surrogates and in-context regression

### OptFormer / Embed-then-Regress

- **Repository:** **optformer/embed_then_regress**, https://github.com/google-research/optformer/tree/main/optformer/embed_then_regress.
- **LLM–BO relationship:** Embed-then-Regress serializes arbitrary inputs as strings, embeds them with a pretrained language model, and performs in-context/general-purpose regression for BO, reporting performance comparable to GP-based methods on synthetic, combinatorial, and hyperparameter-optimization tasks. (nguyen2024predictingfromstrings pages 16-17)
- **Paper:** Tung Nguyen, Qiuyi Zhang, Bangding Yang, Chansoo Lee, Jörg Bornschein, Yingjie Miao, Sagi Perel, Yutian Chen, and Xingyou Song, “Predicting from Strings: Language Model Embeddings for Bayesian Optimization,” *arXiv*, 2024. DOI: **10.48550/arXiv.2410.10190**.

### LLAMBO

- **Repository:** LLAMBO; the exact repository URL was not exposed in the retrieved paper text.
- **LLM–BO relationship:** LLAMBO formulates warm-starting, surrogate prediction, and candidate sampling as in-context language tasks and compares the resulting optimizer with BoTorch GP, deep-kernel GP, TPE, SMAC, HEBO, TuRBO, and other BO/HPO baselines. (akke2025bayesianoptimizationfor pages 2-3, liu2024largelanguagemodels pages 30-31)
- **Paper:** Tennison Liu, Nicolás Astorga, Nabeel Seedat, and Mihaela van der Schaar, “Large Language Models to Enhance Bayesian Optimization,” *The Twelfth International Conference on Learning Representations (ICLR)*, 2024. DOI: **10.48550/arXiv.2402.03921**.
- **Relevance caveat:** LLAMBO is a general BO framework rather than chemistry-specific software, but it is foundational for later chemistry/materials implementations and evaluations.

### BO-ICL — Bayesian Optimization of Catalysis with In-Context Learning

- **Repository:** BO-ICL; no exact repository URL was recovered from the retrieved article or supporting-information pages.
- **LLM–BO relationship:** BO-ICL uses an LLM as the regression surrogate inside a BO loop by retrieving informative in-context examples for each candidate; it compares this surrogate against GPR, kernel ridge regression, and nearest-neighbor models on catalysis and molecular-property datasets. (ramos2026bayesianoptimizationof pages 37-42, ramos2026bayesianoptimizationof pages 17-18)
- **Paper:** Mayk Caldas Ramos, Shane S. Michtavy, Andrew D. White, and Marc D. Porosoff, “Bayesian Optimization of Catalysis with In-Context Learning,” *ACS Central Science* **12**, 599–615, 2026. DOI: **10.1021/acscentsci.5c02418**. (ramos2026bayesianoptimizationof pages 17-18)

### Molecular LLM surrogates / “A Sober Look” implementation

- **Repository:** Repository URL not recovered from the retrieved primary text.
- **LLM–BO relationship:** This implementation evaluates fixed LLM feature extractors and parameter-efficiently fine-tuned Bayesian/Laplace surrogates for molecular BO, finding that chemistry-pretrained or chemistry-fine-tuned models are useful but generic LLMs generally are not; it compares expected improvement and Thompson sampling across six real chemistry datasets. (kristiadi2024asoberlook pages 18-20)
- **Paper:** Agustinus Kristiadi, Felix Strieth-Kalthoff, Marta Skreta, Pascal Poupart, Alán Aspuru-Guzik, and Geoff Pleiss, “A Sober Look at LLMs for Material Discovery: Are They Actually Good for Bayesian Optimization Over Molecules?” *arXiv*, 2024. DOI: **10.48550/arXiv.2402.05015**.

## 3. Benchmarks comparing LLM optimizers with BO

### Coscientist

- **Repository:** **coscientist**, https://github.com/gomesgroup/coscientist. The public repository is explicitly described as a simpler implementation plus generated outputs used in quantitative analyses. (boiko2023autonomouschemicalresearch pages 10-13)
- **LLM–BO relationship:** Coscientist is a GPT-4-driven chemistry agent that plans and executes experiments using search, code, and laboratory-automation tools; its reaction-optimization behavior was directly benchmarked against standard BO rather than embedding BO as its own optimizer. (boiko2023autonomouschemicalresearch pages 10-13)
- **Paper:** Daniil A. Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes, “Autonomous Chemical Research with Large Language Models,” *Nature* **624**, 570–578, 2023. DOI: **10.1038/s41586-023-06792-0**. (boiko2023autonomouschemicalresearch pages 10-13)

### LLM-GO reaction-optimization benchmark

- **Repository:** LLM-GO/platform repository URL was not recovered from the retrieved primary text.
- **LLM–BO relationship:** The study benchmarks knowledge-driven LLM optimizers against traditional chemical-reaction BO and reports that LLM-GO can outperform BO on complex categorical reaction spaces while maintaining a more consistent exploratory bias. (macknight2025pretrainedknowledgeelevates pages 19-23)
- **Paper:** Robert MacKnight, Jose Emilio Regio, Jeffrey G. Ethier, Luke A. Baldwin, and Gabe Gomes, “Pre-trained Knowledge Elevates Large Language Models beyond Traditional Chemical Reaction Optimizers,” *arXiv*, 2025. DOI: **10.48550/arXiv.2509.00103**. (macknight2025pretrainedknowledgeelevates pages 19-23)

### Scientific-domain LLM-vs-BO benchmark

- **Repository:** Exact repository URL was not recovered.
- **LLM–BO relationship:** The benchmark evaluates LLM agents as sequential optimizers against BO on gene-perturbation and molecular-property discovery—including ESOL, FreeSolv, and ionization-energy tasks—and documents validity and search-space-sensitivity failures. (gupta2509llmsforbayesian pages 27-29)
- **Paper:** Rushil Gupta, Jason S. Hartford, and Bang Liu, “LLMs for Bayesian Optimization in Scientific Domains: Are We There Yet?” *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2025. DOI: **10.48550/arXiv.2509.21403**.

### BOPE-GPT and ScattBO — BO Hackathon projects

- **Repository hub:** **Acceleration Consortium BO Hackathon**, https://ac-bo-hackathon.github.io/; individual project links are hosted from the project pages, but exact GitHub URLs for BOPE-GPT and ScattBO were not present in the retrieved paper text.
- **BOPE-GPT:** Uses GPT-4 to supply pairwise output preferences inside BoTorch preferential BO with Expected Utility acquisition for Fischer–Tropsch optimization; it matched explicit-utility BO on simpler cases but underperformed on a harder three-objective problem. (baird2025bayesianoptimizationhackathon pages 11-12)
- **ScattBO:** A Python benchmark that simulates a scattering-based materials self-driving laboratory; it is primarily a BO/SDL benchmark rather than a complete LLM optimizer, but belongs in the ecosystem used to evaluate LLM copilots or agents. (baird2025bayesianoptimizationhackathon pages 11-12)
- **Associated report:** Sterling Baird, Mehrad Ansari, Zartashia Afzal, Qianxiang Ai, Alexander Al-Feghali, Mathieu Alain, Matias Altamirano, Thomas Andrews, Andy Sode Anker, Rija Ansari, Samuel Ampofo Appiah, Raul Astudillo, Ruhana Azam, Mohammed Azzouzi, Suneel Kumar BVS, Ben Blaiszik, Anna Borisova, Andrés Bran, Pengfei Cai, Ting-Yeh Chen, Curtis Chong, Samantha Corapi, Mark Croxall, Gbetondji Dovonon, Jose Manuel Napoles Duarte, Andrew Falkowski, Giuseppe Fisicaro, Martin Fitzner, Quinn Gallagher, Sabah Gaznaghi, Jerome Genzling, Christoph Griehl, Ryan-Rhys Griffiths, Taicheng Guo, Kehan Guo, Nipun Gupta, Ankur Gupta, Mohammad Haddadnia, Yuyang Han, Joscha Hoche, Alexander V. Hopp, Marko Huang, Ayodeji Ijishakin, Ramsey Issa, Yeonghun Kang, Jungtaek Kim, Akshay Kudva, Ruben Laplaza, Magdalena Lederbauer, Shi Xuan Leong, Paul W. Leu, Viola Muning Li, Mingxuan Li, Tao Liu, Stanley Lo, Jakub Lala, Osman Mamun, Owen Melville, Michail Mitsakis, Cameron Movassaghi, Madhav Reddy Muthyala, Marcel Muller, Bozhao Nan, Duc Nguyen, Daniele Ongari, Anthony Onwuli, Can Ozkan, Sergio Pablo-Garcia, Elton Pan, Ratish Panda, Sean Park, Jaehee Park, Dieter Plessers, Tobias Plotz, Ella M. Rajaonson, Bojana Rankovic, Jarett Ren, Rim Rihana, Jurgis Ruza, Akhil S. Nair, Carter Salbego, Erick Lopez Saldivar, Arifin San, Christina Schenk, Stefan P. Schmid, Dylan Schubert, Philippe Schwaller, Cher-Tian Ser, Maitreyee Sharma Priyadarshini, Yuxin Shen, Kevin Shen, Jiale Shi, Farshud Sorourifar, Adrian Sosic, Taylor Sparks, Jan Christopher Spies, Felix Strieth-Kalthoff, Suraj Sudhakar, Aditya Sundar, Alessio Tamburro, Clara Tamura, Yifeng Tang, Dandan Tang, Nikhil Thota, Mohammad Erfan Toloue Sadegh Azadi, Gary Tom, Sang Truong, Ricardo Valencia Albornoz, Luis Walter, Lawrence Wang, Fanjin Wang, Andrew Wang, Yiran Wang, Jeffrey Watchorn, Benjamin Weiser, Geemi Wellawatte, Alexander Wieczorek, Tim Wurger, Ilya Yakavets, Jakob Zeitler, Sylvester Zhang, Yimu Zhao, Yanqiao Zhu, Ruijie Zhu, and Yunheng Zou, “Bayesian Optimization Hackathon for Chemistry and Materials,” *ChemRxiv*, 2025. DOI: **10.26434/chemrxiv-2025-dzh5z**. (baird2025bayesianoptimizationhackathon pages 11-12)

## 4. LLM copilots and agents around BO libraries

### Honegumi RAG Assistant

- **Repository:** An exact public repository URL was not recovered from the available primary material.
- **LLM–BO relationship:** Honegumi is an agentic retrieval-augmented assistant intended to lower the barrier to adopting BO in experimental science by helping users formulate optimization problems and use BO software; it is a copilot around BO rather than a new surrogate or acquisition function.
- **Paper:** Hasan Muhammad Sayeed, Arin Soneji, Sterling Baird, and Taylor Sparks, “Honegumi RAG Assistant: An Agentic System for Accelerating Bayesian Optimization Adoption in Experimental Sciences,” *ChemRxiv*, 2025. DOI: **10.26434/chemrxiv-2025-f1wcr**.

### Biochemical-discovery agent using statistical BO tools

The clearest verified example of an LLM agent actually orchestrating a statistical BO implementation is **LLM4BO**: its molecular workflow gives the LLM access to chemical utilities, validity filters, and statistical BO as callable tools rather than asking the language model to emulate every numerical component internally. (akke2025bayesianoptimizationfor pages 2-3, akke2025bayesianoptimizationfor pages 10-12) This is the most directly relevant open implementation found for the requested “LLM agent orchestrating BoTorch/Ax or BayBE-like libraries” category. The retrieved literature also notes that standard open-source libraries such as BoTorch, Ax, and BayBE are the underlying numerical ecosystem for agentic experimental-design workflows, but a distinct verified repository explicitly wrapping all three with an LLM was not located in the evidence set.

## Consolidated repository list

### Exact repository URLs verified in primary sources

1. **LLM4BO** — https://github.com/learningmatter-mit/LLM4BO — biochemical/molecular/protein LLM+BO benchmark and agentic workflows. (akke2025bayesianoptimizationfor pages 10-12)
2. **LLINBO / LLM-in-the-Loop-BO** — https://github.com/UMDataScienceLab/LLM-in-the-Loop-BO — hybrid LLM exploration plus GP/statistical-BO exploitation.
3. **OptFormer: Embed-then-Regress** — https://github.com/google-research/optformer/tree/main/optformer/embed_then_regress — language-model string embeddings and regression as a general BO surrogate. (nguyen2024predictingfromstrings pages 16-17)
4. **Coscientist** — https://github.com/gomesgroup/coscientist — chemistry agent and self-driving-lab prototype benchmarked against standard BO. (boiko2023autonomouschemicalresearch pages 10-13)
5. **Acceleration Consortium BO Hackathon hub** — https://ac-bo-hackathon.github.io/ — project index covering BOPE-GPT, ScattBO, and related chemistry/materials BO software. (baird2025bayesianoptimizationhackathon pages 11-12)

### Relevant open-software projects for which the exact repository URL was not recoverable from retrieved primary text

6. **BORA** — hybrid language-guided BO research assistant. (cisse2025languagebasedbayesianoptimization pages 1-2, cisse2025languagebasedbayesianoptimization pages 24-25)
7. **LLAMBO** — in-context LLM warm-starting, surrogate modeling, and candidate generation for BO. (akke2025bayesianoptimizationfor pages 2-3, liu2024largelanguagemodels pages 30-31)
8. **GOLLuM** — jointly trained LLM deep kernel and GP surrogate for chemistry BO. (rankovic2504gollumgaussianprocess pages 2-4)
9. **BO-ICL** — in-context LLM surrogate for catalysis and molecular-property BO. (ramos2026bayesianoptimizationof pages 37-42, ramos2026bayesianoptimizationof pages 17-18)
10. **A Sober Look / molecular LLM-surrogate implementation** — fixed and fine-tuned chemistry-language-model features with Bayesian/Laplace surrogates. (kristiadi2024asoberlook pages 18-20)
11. **LLM-GO** — LLM chemical-reaction optimizer benchmarked against traditional BO. (macknight2025pretrainedknowledgeelevates pages 19-23)
12. **Scientific-domain LLM-vs-BO benchmark** — molecular-property and gene-perturbation optimization benchmark. (gupta2509llmsforbayesian pages 27-29)
13. **BOPE-GPT** — GPT-4 preference elicitation inside BoTorch preferential BO. (baird2025bayesianoptimizationhackathon pages 11-12)
14. **ScattBO** — simulated materials self-driving-laboratory benchmark. (baird2025bayesianoptimizationhackathon pages 11-12)
15. **Honegumi RAG Assistant** — LLM copilot for experimental scientists adopting BO.

## Overall assessment

The most mature open patterns are: **LLM as a knowledge/proposal module while a GP remains responsible for uncertainty** (BORA, LLINBO, LLM4BO); **LLM representation or in-context regression as the surrogate** (GOLLuM, Embed-then-Regress, BO-ICL, molecular LLM surrogates); and **LLM agents benchmarked against rather than fused with BO** (Coscientist, LLM-GO, scientific-domain benchmarks). The chemistry evidence consistently cautions that generic LLMs are not automatically superior: chemistry-specific pretraining or fine-tuning, explicit statistical uncertainty, validity filters, and tool-mediated hybridization are generally the strongest designs. (akke2025bayesianoptimizationfor pages 2-3, kristiadi2024asoberlook pages 18-20, akke2025bayesianoptimizationfor pages 10-12)

References

1. (akke2025bayesianoptimizationfor pages 10-12): Mattias Akke, Soojung Yang, Jurgis Ruza, Jinyeop Song, Elton Pan, and Rafael Gomez-Bombarelli. Bayesian optimization for biochemical discovery with llms. ChemRxiv, Nov 2025. URL: https://doi.org/10.26434/chemrxiv-2025-w1wsh, doi:10.26434/chemrxiv-2025-w1wsh. This article has 5 citations.

2. (chang2025llinbotrustworthyllmintheloop pages 21-23): Chih-Yu Chang, Milad Azvar, C. Okwudire, and R. Kontar. Llinbo: trustworthy llm-in-the-loop bayesian optimization. ArXiv, May 2025. URL: https://doi.org/10.48550/arxiv.2505.14756, doi:10.48550/arxiv.2505.14756. This article has 16 citations.

3. (nguyen2024predictingfromstrings pages 16-17): Tung Nguyen, Qiuyi Zhang, Bangding Yang, Chansoo Lee, Jorg Bornschein, Yingjie Miao, Sagi Perel, Yutian Chen, and Xingyou Song. Predicting from strings: language model embeddings for bayesian optimization. ArXiv, Oct 2024. URL: https://doi.org/10.48550/arxiv.2410.10190, doi:10.48550/arxiv.2410.10190. This article has 1 citations.

4. (boiko2023autonomouschemicalresearch pages 10-13): Daniil A. Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. Autonomous chemical research with large language models. Nature, 624:570-578, Dec 2023. URL: https://doi.org/10.1038/s41586-023-06792-0, doi:10.1038/s41586-023-06792-0. This article has 1929 citations and is from a highest quality peer-reviewed journal.

5. (cisse2025languagebasedbayesianoptimization pages 1-2): Abdoulatif Ciss'e, Xenophon Evangelopoulos, Vladimir V. Gusev, and Andrew I. Cooper. Language-based bayesian optimization research assistant (bora). ArXiv, Jan 2025. URL: https://doi.org/10.48550/arxiv.2501.16224, doi:10.48550/arxiv.2501.16224. This article has 16 citations.

6. (cisse2025languagebasedbayesianoptimization pages 24-25): Abdoulatif Ciss'e, Xenophon Evangelopoulos, Vladimir V. Gusev, and Andrew I. Cooper. Language-based bayesian optimization research assistant (bora). ArXiv, Jan 2025. URL: https://doi.org/10.48550/arxiv.2501.16224, doi:10.48550/arxiv.2501.16224. This article has 16 citations.

7. (akke2025bayesianoptimizationfor pages 2-3): Mattias Akke, Soojung Yang, Jurgis Ruza, Jinyeop Song, Elton Pan, and Rafael Gomez-Bombarelli. Bayesian optimization for biochemical discovery with llms. ChemRxiv, Nov 2025. URL: https://doi.org/10.26434/chemrxiv-2025-w1wsh, doi:10.26434/chemrxiv-2025-w1wsh. This article has 5 citations.

8. (rankovic2504gollumgaussianprocess pages 2-4): Bojana Rankovi'c and Philippe Schwaller. Gollum: gaussian process optimized llms - reframing llm finetuning through bayesian optimization. ArXiv, Apr 2504. URL: https://doi.org/10.48550/arxiv.2504.06265, doi:10.48550/arxiv.2504.06265. This article has 5 citations.

9. (rankovic2504gollumgaussianprocess pages 37-38): Bojana Rankovi'c and Philippe Schwaller. Gollum: gaussian process optimized llms - reframing llm finetuning through bayesian optimization. ArXiv, Apr 2504. URL: https://doi.org/10.48550/arxiv.2504.06265, doi:10.48550/arxiv.2504.06265. This article has 5 citations.

10. (liu2024largelanguagemodels pages 30-31): Tennison Liu, Nicolás Astorga, Nabeel Seedat, and Mihaela van der Schaar. Large language models to enhance bayesian optimization. ArXiv, Feb 2024. URL: https://doi.org/10.48550/arxiv.2402.03921, doi:10.48550/arxiv.2402.03921. This article has 252 citations.

11. (ramos2026bayesianoptimizationof pages 37-42): Mayk Caldas Ramos, Shane S. Michtavy, Andrew D. White, and Marc D. Porosoff. Bayesian optimization of catalysis with in-context learning. ACS Central Science, 12:599-615, Apr 2026. URL: https://doi.org/10.1021/acscentsci.5c02418, doi:10.1021/acscentsci.5c02418. This article has 96 citations and is from a highest quality peer-reviewed journal.

12. (ramos2026bayesianoptimizationof pages 17-18): Mayk Caldas Ramos, Shane S. Michtavy, Andrew D. White, and Marc D. Porosoff. Bayesian optimization of catalysis with in-context learning. ACS Central Science, 12:599-615, Apr 2026. URL: https://doi.org/10.1021/acscentsci.5c02418, doi:10.1021/acscentsci.5c02418. This article has 96 citations and is from a highest quality peer-reviewed journal.

13. (kristiadi2024asoberlook pages 18-20): Agustinus Kristiadi, Felix Strieth-Kalthoff, Marta Skreta, Pascal Poupart, Alán Aspuru-Guzik, and Geoff Pleiss. A sober look at llms for material discovery: are they actually good for bayesian optimization over molecules? ArXiv, Feb 2024. URL: https://doi.org/10.48550/arxiv.2402.05015, doi:10.48550/arxiv.2402.05015. This article has 83 citations.

14. (macknight2025pretrainedknowledgeelevates pages 19-23): R. MacKnight, Jose Emilio Regio, Jeffrey G. Ethier, Luke A. Baldwin, and Gabe Gomes. Pre-trained knowledge elevates large language models beyond traditional chemical reaction optimizers. ArXiv, Aug 2025. URL: https://doi.org/10.48550/arxiv.2509.00103, doi:10.48550/arxiv.2509.00103. This article has 6 citations.

15. (gupta2509llmsforbayesian pages 27-29): Rushil Gupta, Jason S. Hartford, and Bang Liu. Llms for bayesian optimization in scientific domains: are we there yet? ArXiv, Sep 2509. URL: https://doi.org/10.48550/arxiv.2509.21403, doi:10.48550/arxiv.2509.21403. This article has 17 citations.

16. (baird2025bayesianoptimizationhackathon pages 11-12): Sterling Baird, Mehrad Ansari, Zartashia Afzal, Qianxiang Ai, Alexander Al-Feghali, Mathieu Alain, Matias Altamirano, Thomas Andrews, Andy Sode Anker, Rija Ansari, Samuel Ampofo Appiah, Raul Astudillo, Ruhana Azam, Mohammed Azzouzi, Suneel Kumar BVS, Ben Blaiszik, Anna Borisova, Andres Bran, Pengfei Cai, Ting-Yeh Chen, Curtis Chong, Samantha Corapi, Mark Croxall, Gbetondji Dovonon, Jose Manuel Napoles Duarte, Andrew Falkowski, Giuseppe Fisicaro, Martin Fitzner, Quinn Gallagher, Sabah Gaznaghi, Jerome Genzling, Christoph Griehl, Ryan-Rhys Griffiths, Taicheng Guo, Kehan Guo, Nipun Gupta, Ankur Gupta, Mohammad Haddadnia, Yuyang Han, Joscha Hoche, Alexander V. Hopp, Marko Huang, Ayodeji Ijishakin, Ramsey Issa, Yeonghun Kang, Jungtaek Kim, Akshay Kudva, Ruben Laplaza, Magdalena Lederbauer, Shi Xuan Leong, Paul W. Leu, Viola Muning Li, Mingxuan Li, Tao Liu, Stanley Lo, Jakub Lala, Osman Mamun, Owen Melville, Michail Mitsakis, Cameron Movassaghi, Madhav Reddy Muthyala, Marcel Muller, Bozhao Nan, Duc Nguyen, Daniele Ongari, Anthony Onwuli, Can Ozkan, Sergio Pablo-Garcia, Elton Pan, Ratish Panda, Sean Park, Jaehee Park, Dieter Plessers, Tobias Plotz, Ella M. Rajaonson, Bojana Rankovic, Jarett Ren, Rim Rihana, Jurgis Ruza, Akhil S. Nair, Carter Salbego, Erick Lopez Saldivar, Arifin San, Christina Schenk, Stefan P. Schmid, Dylan Schubert, Philippe Schwaller, Cher-Tian Ser, Maitreyee Sharma Priyadarshini, Yuxin Shen, Kevin Shen, Jiale Shi, Farshud Sorourifar, Adrian Sosic, Taylor Sparks, Jan Christopher Spies, Felix Strieth-Kalthoff, Suraj Sudhakar, Aditya Sundar, Alessio Tamburro, Clara Tamura, Yifeng Tang, Dandan Tang, Nikhil Thota, Mohammad Erfan Toloue Sadegh Azadi, Gary Tom, Sang Truong, Ricardo Valencia Albornoz, Luis Walter, Lawrence Wang, Fanjin Wang, Andrew Wang, Yiran Wang, Jeffrey Watchorn, Benjamin Weiser, Geemi Wellawatte, Alexander Wieczorek, Tim Wurger, Ilya Yakavets, Jakob Zeitler, Sylvester Zhang, Yimu Zhao, Yanqiao Zhu, Ruijie Zhu, and Yunheng Zou. Bayesian optimization hackathon for chemistry and materials. Jun 2025. URL: https://doi.org/10.26434/chemrxiv-2025-dzh5z, doi:10.26434/chemrxiv-2025-dzh5z. This article has 2 citations.