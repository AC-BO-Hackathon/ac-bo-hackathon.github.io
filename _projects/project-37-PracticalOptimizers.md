---
number: 37 # leave as-is, maintainers will adjust
title: The Effects of Post-Modelling Performance Metric Computation on the Efficiency of Bayesian Optimizers
topic: general
team_leads:
  - Thomas Andrews (The University of Melbourne, CSIRO) @TSAndrews

# Comment these lines by prepending the pound symbol (#) to each line to hide these elements
# contributors:
#  - Contributor 1 (Institution 1)
#  - Contributor 2 (Institution 2)

github: TSAndrews/EmbeddedKnowledgeBO
youtube_video: kwXHoWV8g1E

---

## Introduction
Bayesian optimization is often considered a black-box technique, however several simple modifications to 
the design can vastly increase the optimizers computational and iterative performance on certain tasks. The
modification explored here relates to what aspects of a problem are actually modelled during the optimization 
procedure. Raw data collected is not typically in a form that properly represents the value of the systems 
state and often needs to be transformed into one or more performance metrics that are desired to be optimized.
Traditionally, these performance metrics are what get modelled during the Bayesian optimization process but this 
leads to a loss of the structural knowledge introduced by the transforms. If the parameters being optimized 
are featured in the performance calculations, knowledge of these influences are lost from the system. Modelling 
only the raw data may also reduce the number of models that need be fitted in multi-objective problems. There is 
no need to create a separate model for each if metrics if they are derived from the same raw data. This can 
result in significant computational savings for the optimization runs. Another potential benefit lies with the
form of the models themselves. Many performance metrics increase the complexity of the models. This increase in
complexity could degrade the fit of the models, and result in a decrease in the overall performance of the 
optimizer. The form of raw data models are also likely to be better understood by domain experts which could 
also increase the ease of designing covariance kernels that are better suited to the data. 

The impacts of performance metric computation order on computational and iterative efficiency were investigated using
the optimization of a simulated nucleophilic aromatic substitution reaction system as a case study. This simulated 
system was adapted from the summit software package<sup>1</sup> and is based on the works of Hone et 
al.<sup>2</sup>. The system was optimized to maximize space-time yield and minimize reaction E-factor. 
These are common industrial measures for production rate and material wastage respectively. Both of these
metrics can be calculated from the concentration of product produced by a reaction and the set experimental 
parameters such as duration and initial reactant quantities.

## Results
Computation of performance metrics from a single model for yield halved the computation time for each iteration of 
the optimizer compared to modelling both space-time yield and E-factor separately. This is to be expected. 
Model fitting is typically the most computationally intensive task during Bayesian optimization and so 
reducing the number of models that need be fitted has a significant impact on computation time.

Post-modelling performance metric computation does not appear to have a significant impact on the convergence rate of 
the optimizer. When data has a low noise level, post-modelling performance metric computation does typically increase
hypervolume more rapidly than computing performance metrics prior to modelling in early iterations, as can be seen from Figure 1, but this lead is 
lost fairly quickly and both objective computation methods generally reach the optima at the same
time. This is because post-modelling performance metric computation biases selection toward regions that have
high value experimental conditions based on the metrics without considering the responses of the system under these conditions.
For instance, the optimizer will be biased towards low residence times because time is a key component of space time yield, but
these conditions are not necessarily optimal because residence time and yields are inversely proportional. As such, the optima of
the system may not lie at minimal residence times if the drop in yields exceed the increase in speed. Post-modelling computation 
gets an early lead due to its better understanding of the impact of the impact of reactor parameters on the metrics values, but it
still needs to determine the effects of yields to determine the optima. The early bias likely hinders exploration of the domain
counteracting the benefits of increased knowledge integration as iterations progress. 

![Plot of hypervolume improvement against iteration number](https://github.com/TSAndrews/EmbeddedKnowledgeBO/blob/b9df31f1587068a08dc98b9ba5ce14b0cd856056/results/HypervolumePlotMetricCompOrder.png?raw=True)
*Figure 1: Plot of hypervolume improvement against iteration number for post-modelling performance metric computation (orange line) and pre-modelling metric computation (blue dashed)*

The drawbacks of the bias introduced by post-modelling metric computation could likely be counteracted by more intelligent design
of the priors of the optimizer. It is typically known that yields are likely to decrease with decreasing residence time which would
counteract the low residence time bias being introduced by the space time yield performance metric. The bias may even be useful in 
most systems by enabling domain reduction. There is a known upper bound for yields as we cannot create matter. This means that it 
can be known that increasing residence time cannot possibly improve metrics such as space time yield because yields may need to be
greater than possible in order to counteract the time effects. Biasing exploration towards regions of short residence 
time increases the likelihood of being able to reduce the domain size.

## Conclusions
Computing performance metrics after modelling can significantly reduce computation time if multiple metrics are derived from the same
measurements. These improvements will be especially noticeable for problems with a large number of metrics to be optimized based on only 
a few different sensors.
Computing performance metrics after modelling increases the early rate of improvement of the system due to the increased knowledge of
the effects of reactor parameters on the metrics, but this early bias likely decreases exploration rate, and thus does little to improve
the overall optimization times. It’s possible that these drawbacks could be overcome by the use of non-constant priors or by merely 
enforcing a spacing criterion during experimental selection in early iterations. 

This research only serves as a precursory study of the effects of post modelling metric computation. There was insufficient 
exploration of benchmarks or algorithm parameters to have a strong confidence in the findings. Further research is still required.

Check out our social media post on [LinkedIn](https://www.linkedin.com/posts/thomas-andrews-177473143_can-the-performance-of-bayesian-optimizers-activity-7183059284807593984-BHdh?utm_source=share&utm_medium=member_desktop)!

## References:
1. Felton, K. C., Rittig, J. G., & Lapkin, A. A. (2021), [Summit: benchmarking machine learning methods for reaction optimisation](https://doi.org/10.1002/cmtd.202000051). _Chemistry‐Methods_, _1_(2), 116-122.
2. Hone, C. A., Holmes, N., Akien, G. R., Bourne, R. A., & Muller, F. L. (2017). [Rapid multistep kinetic model generation from transient flow data](https://doi.org/10.1039/C6RE00109B). _Reaction chemistry & engineering_, _2_(2), 103-108.
