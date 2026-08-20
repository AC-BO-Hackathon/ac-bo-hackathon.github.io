---
number: 33 # leave as-is, maintainers will adjust
title: Bayesian Optimization for Hyperspectral Co-heritability Search 
topic: benchmark-task
team_leads:
  - Ruhana Azam (University of Illinois Urbana-Champaign)
  - Sang T. Truong (Stanford University)

# Comment these lines by prepending the pound symbol (#) to each line to hide these elements
contributors:
#  - Contributor 1 (Institution 1)
#  - Contributor 2 (Institution 2)

github: stair-lab/bo4ag
# youtube_video: <your-video-id>

---

Genomic prediction models are often used to predict which crops may be good selections for the next round of breeding. This is done to improve plant resilience to pests and climate change and increase yield. Our interest is in finding good proxy data for training genomic prediction models. The proxy data we are interested in is wavelength ratios. The "goodness" of the proxy can be measured by a measure called co-heritability. Co-heritability is expensive enough to calculate such that brute force is impractical. The goal of this project is to benchmark BO as a way to find wavelength ratios with high co-heritability. The work is an extension of the a previous workshop paper [1].

References:
[1] Ruhana Azam, Sang T. Truong, Samuel B. Fernandes, Andrew D.B. Leakey, Alexander Lipka, Mohammed El-Kebir, Sanmi Koyejo. "Pretraining Probabilistic Models for Scalable Precision Agriculture". In ICLR 2024 Workshop on Data-centric Machine Learning Research (DMLR): Harnessing Momentum for Science. URL: [https://openreview.net/pdf?id=tPPm5OKdFy](https://openreview.net/pdf?id=tPPm5OKdFy)
