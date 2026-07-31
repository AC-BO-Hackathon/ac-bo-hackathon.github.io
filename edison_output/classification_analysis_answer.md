## Project-level meta-analysis

The manuscript describes **41 submitted projects, not 45**. Project identifiers run to 45, but IDs **14, 19, 29, and 42 are absent**. I therefore used the 41 projects actually listed and did not invent four missing projects. Two listed projects, **#23 and #34**, lack full narrative descriptions in the supplied manuscript; those two were coded conservatively from their titles and surrounding manuscript context.

This is a qualitative content analysis, not a statistical meta-analysis of effect sizes. The projects use different objectives, datasets, budgets, baselines, and performance measures, so pooling numerical performance would be invalid.

### (a) Primary output categories

Each project was assigned exactly one primary category according to its main hackathon deliverable.

| Primary output category | Projects | Count | Share of 41 |
|---|---|---:|---:|
| Application demonstration | 6, 7, 8, 9, 13, 16, 17, 18, 21, 22, 25, 26, 27, 30, 32, 34, 37, 38, 39, 40, 44 | **21** | **51.2%** |
| Preliminary concept | 2, 3, 15, 20, 23, 36, 41 | **7** | **17.1%** |
| Benchmark dataset/problem | 1, 5, 24, 28, 33, 45 | **6** | **14.6%** |
| Tutorial/educational | 10, 12, 31, 43 | **4** | **9.8%** |
| Mature software | 4, 11, 35 | **3** | **7.3%** |
| **Total** |  | **41** | **100%** |

“Mature software” is used here as the closest of the requested categories for a usable, released tool or an extension to an established library. It should **not** be read as evidence of production readiness. In particular, SimpleGPT-BO (#4) and BlendDS (#11) were hackathon-scale software outputs; GAUCHE (#35) was already an established library, with the hackathon contributing input warping and tutorials.

The central pattern is clear: approximately half the submissions were **application demonstrations**, while only 3 produced software-like deliverables. This distribution is consistent with a two-day event in which most teams tested feasibility rather than completed validation.

### (b) Dominant domains and recurring frameworks

Using one primary domain per project, the portfolio divides as follows:

| Primary domain | Count |
|---|---:|
| Materials, devices, and self-driving laboratories | **11** |
| Molecular, drug, and protein discovery | **11** |
| Generic BO methods, tools, benchmarks, and education | **11** |
| Chemical reactions and process optimization | **7** |
| Crop genetics | **1** |

Prominent scientific themes included porous materials for gas capture or storage (#9, #39), corrosion and concrete (#7, #12), zeolite and thin-film design (#6, #10), molecular and drug discovery (#8, #17, #21, #25), reaction optimization (#15, #16, #26, #37, #40, #41), and laboratory automation (#20, #24, #30).

Framework counts are based only on **explicit statements in the project descriptions**:

- **BoTorch:** directly used by #1 and #16; #26 used BayBE, explicitly described as built on BoTorch. Thus the broader BoTorch ecosystem appears in **3 projects**, but direct BoTorch use is documented in **2**.
- **BayBE:** **2 projects**, #7 and #26.
- **Dragonfly:** #1 only.
- **BayesO:** #6 only.
- **scikit-optimize:** #30 only.
- **Ax:** #31 only.
- **GAUCHE:** #35 only.
- **Optuna:** #38 only.
- **Gryffin/Atlas:** no explicit use was reported in the supplied project narratives.

Thus, BoTorch and BayBE were the only named BO frameworks that clearly recurred across teams. Framework use is underreported because many descriptions specify Gaussian processes or acquisition functions without naming the software implementation.

### (c) Common methods and important differences

**Common choices**

- **Gaussian-process surrogates dominated.** They were used in conventional form, with robust likelihoods for outliers (#12), specialized molecular kernels (#22, #35), local models after clustering (#39), and multi-output or multi-objective settings (#1, #6, #16, #18).
- **Acquisition functions covered the standard BO toolkit:** expected improvement, probability of improvement, upper confidence bound, Thompson sampling, expected hypervolume improvement, q-noisy expected hypervolume improvement, ParEGO/random scalarization, expected utility, and epsilon-greedy selection.
- **Random search was the main baseline.** Several projects showed improvement over random selection (#5, #7, #9, #17, #33, #44), but #33 found standard GP-based BO performed similarly to random search.
- **Chemical representation was treated as a first-order design choice.** Teams compared MACCS, RDKit, Mordred, Morgan/extended-connectivity fingerprints, learned MolFormer representations, graph representations, and direct similarity or distance kernels (#7, #8, #17, #21, #22, #25, #27).
- **Most studies were retrospective or simulated.** They replayed BO on fixed datasets or analytic functions. The notable laboratory-in-the-loop example was voltammetry waveform optimization (#30); hydrogel automation (#20) was primarily a proposed workflow.

**Differences among approaches**

- **Single versus multiple objectives:** projects ranged from scalar property optimization to Pareto-front methods (#1, #6, #18), preference-based multi-output optimization (#16), and conditions intended to generalize across related tasks (#45).
- **Myopic versus planning-aware selection:** most used one-step acquisition functions, whereas #36 explored non-myopic, cost-aware look-ahead.
- **Fixed versus adaptive batching:** #15 explicitly optimized or adapted batch size; #30 used laboratory batches; #31 emphasized asynchronous ask/tell operation.
- **Single versus multiple fidelities or contexts:** #2 examined long-run multifidelity behavior, while #7 and #26 used transfer learning across alloys, campaigns, or reaction temperatures.
- **Surrogate alternatives:** random forests were effective for high-dimensional molecular fingerprints in #17 but unhelpful and computationally heavier in #8. #44 replaced value regression with pairwise ranking, and #33 found a pretrained mixed multitask model better than standard GP BO.
- **Representation and dimensionality handling:** teams used principal component analysis (#8, #27), learned sparse subspaces (#21), clustering plus local GPs (#39), and chemical-distance kernels that avoided vector embeddings (#22).
- **Interpretability and operational realism:** #13 analyzed campaigns over time, #23 addressed noise, #27 studied warm-start design, #37 reduced model-fitting cost by deriving objectives after modeling, and #3 spent more computation optimizing the acquisition function itself.

These contrasting results argue against a universal BO recipe. Surrogate, representation, initialization, and acquisition strategy interacted strongly with dimension, dataset size, noise, and experimental cost.

### (d) LLM and generative-model projects

Under a strict definition, **6 of 41 projects (14.6%)** explored an LLM or a generative model:

- **LLMs or retrieval-augmented LLM systems, 5 projects:** SimpleGPT-BO (#4), natural-language blend-space specification (#11), GPT-4 preference elicitation (#16), multi-agent reaction optimization (#40), and retrieval-augmented BO (#41).
- **Explicit molecular generation, 1 project:** graph-genetic-algorithm-guided de novo drug design (#25).

A broader language-model count is **8 of 41 (19.5%)** if pretrained scientific language-model representations are included: MolFormer fingerprints in #27 and a protein BERT model in #32. Project #15 mentioned LLM retraining only as an example of model cost and was therefore not counted.

The evidence was mixed. LLMs lowered access barriers and helped specify spaces or retrieve warm starts, but GPT-4 preference optimization in #16 degraded on the more complex objective. The multi-agent gains in #40 were demonstration-scale rather than broad validation.

### (e) Collective strengths and limitations of BO

**Strengths revealed by the projects**

1. **Sample efficiency:** BO often located strong candidates faster than random sampling, including MOFs (#9), corrosion inhibitors (#7), molecular candidates (#21), and covalent organic frameworks (#39).
2. **Native uncertainty handling:** posterior uncertainty supported exploration, noisy-objective optimization, and principled ranking of expensive experiments.
3. **Flexibility:** teams handled continuous, categorical, mixed, molecular, multi-objective, multifidelity, contextual, batched, and cost-varying problems.
4. **Ability to incorporate domain knowledge:** chemical descriptors, similarity kernels, prior campaigns, stakeholder preferences, pretrained models, and retrieval systems could all influence proposals.
5. **Compatibility with laboratory workflows:** ask/tell interfaces and batching allowed human or automated experiments to occur between model updates (#20, #30, #31).

**Limitations revealed by the projects**

1. **BO is sensitive to representation and surrogate choice.** GP performance deteriorated in high-dimensional fingerprint spaces (#17), while different molecular descriptors materially changed outcomes (#7, #8, #27).
2. **Default BO was not always superior to simple baselines.** In #33, standard GP BO was comparable to random search; Dragonfly also struggled against random candidates in the narrow benchmark of #1.
3. **Scaling remains difficult.** Large discrete chemical spaces, large datasets, and repeated acquisition optimization can make GPs and acquisition functions expensive (#3, #8, #39).
4. **Transfer and low-fidelity data can hurt.** Multifidelity gains in #2 disappeared over longer budgets, and #26 found that more source data was not necessarily better.
5. **Operational details matter:** initialization, batch size, retraining overhead, noise, outliers, experimental failure, and stopping criteria can determine practical success.
6. **Model optimization is not the same as scientific validation.** Retrospective benchmark gains may not transfer to wet-laboratory campaigns, and docking or scattering proxies may not establish binding or successful synthesis (#24, #25).
7. **LLM integration adds another uncertain component.** Outputs can help with interfaces and priors but can fail on complex preferences and require validation against non-LLM baselines.

The strongest collective conclusion is therefore narrow: the projects show that BO is a flexible way to prioritize expensive evaluations, but performance depends on problem formulation, representation, surrogate, acquisition function, initialization, and cost model. Because the hackathon lasted only **two days**, most findings are proofs of concept based on small experiments, simulations, or retrospective datasets. The reported wins should not be interpreted as stable framework rankings, general superiority over design of experiments, or evidence of real-world scientific acceleration without replication and prospective validation.

*Source: attached manuscript, especially the project list and descriptions on pp. 6–16 and the event description on pp. 2–3.*

### Discretionary analytical decisions

- Treated the manuscript’s 41 listed submissions as the denominator rather than assuming four undocumented projects from the maximum project ID of 45.
- Assigned exactly one primary output category per project, based on its main deliverable; secondary characteristics were not double-counted.
- Used “mature software” for released, usable software or a contribution to an established library, while explicitly separating this coding label from production maturity.
- Coded #23 and #34 conservatively from their titles and manuscript context because full descriptions were absent from the supplied PDF.
- Used one primary application domain per project to make domain counts mutually exclusive.
- Counted software frameworks only when explicitly named; did not infer implementations from acquisition functions or model choices.
- Reported both strict and broad language/generative-model definitions because including MolFormer and protein BERT as “LLMs” is terminologically debatable.
- Did not pool project performance quantitatively because outcomes, evaluation budgets, datasets, and metrics were not commensurate.