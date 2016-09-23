---
title: Simple Bayesian Analysis of High Throughput Biological Measurement Data
authors:
  - name: Eric J. Ma
    affiliation: MIT
  - name: Vivian J. Zhong
    affiliation: MIT
  - name: Islam T. M. Hussein
    affiliation: MIT
  - name: Jonathan A. Runstadler
    affiliation: MIT
target_journal: pnas, plos_comp_bio, biostatistics, plos_one
---

# Abstract

key points:

- describe a simple and accessible framework for HT analysis that is sorely missing from the literature. covers the following:
    - Bayesian estimation of fold changes relative to some control, with decision rule for a hit.
- approach: rather than analytical, use probabilistic programming, with approx. inference tools used.
- accompanying software that analyzes fold change data in an accessible fashion (?)

# Introduction

High throughput (HT) screening experiments are necessary for systematically interrogating biology. Statistical tools have been developed for HT data analysis, for example, the Z- and Z'-factors [@Zhang:1999fr; @Edwards:2015ig; @Lee:2010if; @Sui:2007dc], per-plate Z-score normalization [@Malo:2006kg], ANOVA [@Su:2010gb] and the "three standard deviation" (3-SD) rule-of-thumb [@Zhang:1999fr]. These statistical tools would be useful, if not for the widespread use of small sample sizes [@Edwards:2015ig; @Wang:2015ba] risking the measurement of false positives and negatives.

Crucially missing from the HT literature are general and extensible Bayesian analysis methods for HT assays. Bayesian methods offer several advantages over the traditional Null Hypothesis Significance Testing (NHST) [@Kruschke:2013jy], including the ability to incorporate prior knowledge where appropriate, model and quantify uncertainty in estimated values. As Bayesian analysis returns a full probabilistic description of the data, multiple hypothesis testing is not an issue as any further comparisons are merely extended summaries of the probabilistic output.

To address the problem of a lack of Bayesian analysis methods, we use a probabilistic programming approach to develop a simple Bayesian hierarchical model of a 'generic' HT assay. In this generic assay, the activity of a sample is being determined relative to a blank well and a positive control. Using this simple Bayesian hierarchical model, we are able to simultaneously provide Bayesian posterior distributions of Z-factors for each sample the assay and for the assay in general, dynamic range of the assay, and fold change activity for each sample. We then address is where and when the common experimental practice of duplicate (`n=2`) or triplicate (`n=3`) are sufficient for detecting true hits.

<!-- potential references:

1. Enhancing reproducibility in cancer drug screening: how do we move forward? http://www.ncbi.nlm.nih.gov/pubmed/25015668
1. Linear models and empirical bayes methods for assessing differential expression in microarray experiments. http://www.ncbi.nlm.nih.gov/pubmed/16646809
1. Empirical Bayesian analysis of paired high-throughput sequencing data with a beta-binomial distribution. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658937/
1. Bayesian Analysis of High-Throughput Quantitative Measurement of Protein-DNA Interactions http://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0026105 -->

# Analysis Framework and Simulated Data

<!-- key points:
- experimental setup: a generic "fold change" experiment. To make things concrete, do systematic measurement of protein phenotypes (akin to Stanford HIV DB data.)
    - batch effects are controlled for by having internal controls and standards
    - randomization in position is ideal, but may be difficult to achieve in practice.
    - single replicates per plate, use replicate plate measurements.
    - need figure
- simple Bayesian hierarchical model (BGM) of final readout
- what needs to be modelled, and what can be ignored? By setting things up such that plates are internally consistent, only need to do single replicates per plate, but do replicate plates on different experimental runs.
- error modelled as 95% HPD in posterior distribution -->

If carefully considered, the problem of high throughput measurement at it essence is the measurement and estimation of a sample's real-valued property, relative to a standardized control. These are measured relative to a "blank" that should exhibit a signal below the lower limit of detection, thereby reliably defining what the lower detection limit value is.

# Results

## Modelled Error in estimate as function of number of replicates

key points:
- result: variance in error (modelled mean - real mean) decreases with increasing replicate measurements.
- n=2 or n=3 might not be the best thing to do, especially if uninformative priors are used.
- in general, fold change estimate precision increases with number of samples; error decreases.

## Dealing with outliers


## Small-scale real-world measurement data.

key points:
- put analysis of polymerase assay data here; can even just be Vivian's replication data and that would be sufficient.

# Discussion

## Outliers

## "Precision is the goal"

key points:
- `n=3` + NHST has led to the proliferation of false positive results in the literature.
- `n=some_value` + bayesian can let us identify measurements that have a high degree of uncertainty/variation.
- decision rule is possible: check that 95% HPDs are non-overlapping. alternatively, have a pre-defined ROPE (Kruschke). emphasize: no free lunch.
- deciding whether something is significant should still be on the basis of "biological" significance, not "statistical" significance.
