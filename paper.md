---
title: Bayesian Analysis of High Throughput Data
author:
- name: Eric J. Ma
  affiliation: Department of Biological Engineering, MIT
- name: Islam T. M. Hussein
  affiliation: Department of Biological Engineering, MIT
- name: Vivian J. Zhong
  affiliation: Department of Biological Engineering, MIT
- name: Christopher Bandoro
  affiliation: Microbiology Program, MIT
- name: Jonathan A. Runstadler
  affiliation: Department of Biological Engineering and Division of Comparative Medicine, MIT
target_journal: pnas, nature_biotech, plos_comp_bio, biostatistics, plos_one
toc: True
header-includes:
- \usepackage[left]{lineno}
- \linenumbers
---

# Abstract

Duplicate or triplicate experimental replicates are commonplace in the high throughput literature. However, it has not been tested whether this is statistically defensible or not. To address this issue, we use probabilistic programming to develop a simple hierarchical model for analyzing high throughput measurement data. With the model and simulated data, we show that a small increase in the number of replicate experiments can quantitatively improve accuracy in measurement. We also provide posterior densities for statistical parameters used in the evaluation of HT data. Finally, we provide an extensible open source implementation that ingests data structured in a simple format and produces posterior densities of estimated measurement and assay evaluation parameters.

# Introduction

High throughput (HT) screening experiments are necessary for systematically interrogating biology. However, there are a number of statistical issues that are widespread in the HT screening literature. Firstly, triplicate (or worse, duplicate) measurements are commonplace, with little statistical justification; conceivably, the choice to test as few replicates as possible is most likely cost driven, which is a pragmatic reason but nonetheless detrimental for scientific accuracy. Secondly, t-tests with multiple hypothesis correction serves as the main vehicle for statistical analysis of HT data; multiple hypothesis correction potentially leads to falsely identifying samples as negatives or non-hits. Thirdly, standard error of the mean (SEM) are commonly used as the reported error bars, not only in the HT literature but also in non-HT publications [@Kemnitzer:2005cr; @Marion:2009cm; @LeHellard:2002ht; @Fu:2014jl], and this under-represents the variation in the data. Finally, statistical parameters for assay evaluation are computed without acknowledging the uncertainty that may arise because of uncertainty in the data.

To address these problems, we take an empirical approach. We use probabilistic programming to develop a simple Bayesian hierarchical model of a 'generic' HT assay (Figure @fig:pgm, Supplementary Materials). In this model, the final data of interest (fold change, percentage activity, etc.) are modelled using uninformative priors. Using this model, we are able to simultaneously provide Bayesian posterior distributions of measurement and statistical evaluation parameters. We show, using simulation studies, that increasing the number of replicates by one or two measurements can drastically reduce measurement inaccuracy. Using both simulation and real data, we show that the common practice of reporting mean ± SEM under-represents the uncertainty in measurement variation. We then argue that the uncertainty in statistical assessment parameters can help guide rational decision-making, such as deciding what hits to pursue. Finally, we provide an extensible open source tool for the analysis of such data.

![Bayesian hierarchical model.](./figures/pgm.png){#fig:pgm}

# Results

## Statistically Defensible Replicate Measurements

In order to investigate how the number of replicates affected the accuracy, we simulated experimental runs of 100 samples with varying numbers replicate measurements (`n=2` to `n=20`). For each `n`, 20 experimental runs were simulated.

As shown in Figure @fig:accuracy, the baseline accuracy rate with duplicate (`n=2`) measurements, as measured by fraction of actual values inside the posterior density's 95% HPD, falls around the 70-75% range. This means that about 25% of the final posterior 95% HPDs do not encompass the actual value. By contrast, by using `n=5` replicates, the accurate HPD fraction falls around the 85-90% range. Roughly doubling the number of samples decreases the inaccurate fraction by up to 3-fold. Following the law of diminishing marginal returns, additional accuracy can be gained, but at a cost of increasing sample sizes.

![Accuracy of 95% HPD as a function of number of replicate samples taken.](./figures/accuracy.pdf){#fig:accuracy}

## Representation of Uncertainty

Statistical software (e.g. GraphPad Prism) make it easy for researchers to visualize and compute frequentist confidence intervals and error bars. However, as a result of their ease of use, it is also easy to make statistical errors such as reporting error bars using the standard error of the mean (SEM), rather than 95% confidence/credible intervals. Our analysis of simulation and experimental data show clearly what can be inferred from the mathematical form but is often ignored: that the SEM grossly under-represents the uncertainty in measurement and data variation compared to 95% confidence intervals and Bayesian 95% credible intervals (Figure @fig:range-estimates). The SEM also provides the standard deviation of the sampling distribution of the mean, and not the uncertainty in our measurement of the mean. As such, it would be poor statistical practice to report SEM, and Bayesian 95% credible intervals would be a much preferable choice.

![Bayesian 95% credible interval, Frequentist 95% confidence interval, and SEM interval widths as compared to the actual data range. (left) Simulated data. (right) Experimental measurement data measuring the influence of heat-killed bacteria on influenza activity.](./figures/range-estimates.png){#fig:range-estimates}

## Posterior Densities of Assay Parameters

Statistical parameters, such as the Z-factor, have been developed to evaluate the quality of HT assay data [@Zhang:1999fr; @Sui:2007dc]. By taking a Bayesian view, we can compute not just the expected parameter values but also their posterior distributions (Figure @fig:z-factor), in the same way as distributions on effect sizes can be deterministically computed [@Kruschke:2013jy]. As such, given the uncertainty surrounding the measurements, the original 3-class system for classifying the quality of an hit can be extended to 5 classes (Figure @fig:z-factor). The original 3-class system was "large separation" (Z-factor ≥ 0.5), "small separation" (0 < Z-factor < 0.5) and indistinguishable from noise Z-factor < 0. With a Bayesian view of the data, we can assign credibility to the Z-factor scores, hence allowing for "probable large separation" and "probable small separation", which may be of most practical interest in screening experiments.

![Z-score classes and simulation data. Circle/dot: HPD mean. Thick lines: HPD inter-quartile range. Thin lines: 95% HPD range. (a) Five Z-score classes based on the Z-score posterior density. (b) Forest plot of posterior distributions from one simulation run. Samples 11 and 12 (respectively) are the blank and the non-extreme positive control in this simulated experiment. (top-left) Posterior density in fold change relative to blank. (top-right) Posterior density of variance. (bottom-left) Deterministic posterior density of fold change relative to positive control. (bottom-right) Deterministic posterior density of Z-factor computed using the non-extreme positive control as the baseline.](./figures/z-factor.png){#fig:z-factor}

The actionable consequences of these Z-value distributions depends on the experimental context. There may be scenarios where downstream experimentation is expensive, and only "true hits" should be tested; in this case, the "probable large separation" samples may be chosen for exclusion, helping to reduce costs. On the other hand, if downstream experimentation is cheap, and it is desirable to have a large set of samples to be processed further, then samples in the "probable small separation" may be included in downstream testing, helping to reduce false negatives. The truism remains: statistics does not replace human judgment of the value of a sample, but can serve as a valuable tool in the decision-making process.

We note that Z-factors are not the only statistical parameters that can be computed. Other deterministically calculated parameters, such as effect sizes, can be computed in a similar fashion, likewise yielding uncertainty estimates, given the data.

# Discussion

It is well-known that Bayesian analysis allows the uncertainty in parameter estimates to be explicitly modelled, with credibility (probability density) assigned to parameter estimate intervals. The provision of uncertainty can clarify close-to-call situations (e.g. Z-factors close to 0.5) and uncover potential false positives (e.g. large Z-factors close to > 0.5 but with high variance), enabling better decision-making under uncertainty. Other merits and caveats of Bayesian analysis have been treated extensively in the literature as well [@Kruschke:2013jy; @Lin:1999cd], and we do not go further into them here.

Probabilistic programming approaches make Bayesian methods much more accessible than analytical methods [@Salvatier:2015tb]. By leveraging these tools, we are in turn able to make Bayesian methods more generally accessible for the generic researcher working in high throughput measurement. In aid of reproducible science, we have also released an open source command-line program available for analysis of this type of data (#cite: Zenodo), with a guide available in both the supplementary material and in the archived repository.

A key issue that has cropped up over the past half decade is the scientific "reproducibility crisis", partly due to erroneous researcher reliance on p-values as a judgement device for "significance" [@Wasserstein:2016jo]. Judgements of what "hits" to continue with downstream processing often relies on a calculated p-value rather than effect sizes; statistical significance has come to replace biological significance [@Nuzzo:2014bp; @Baker:2016hd]. In light of this, we argue that by taking a Bayesian view of the data, we may replace p-value-based judgement calls with ones based on the distribution and uncertainty in estimated quality evaluation parameters (e.g. Z-factors & effect sizes), hence improving the quality of published results in the scientific literature.

# Materials and Methods

## Code & Data

All code for simulation and analysis are available as Python scripts and Jupyter notebooks. The archived version used in this publication is released on Zenodo (#TODO), while the source code and data (including that used for this manuscript) can be found on [GitHub](^github).

[^github]: https://github.com/ericmjl/bayesian-measurement-paper

# References
