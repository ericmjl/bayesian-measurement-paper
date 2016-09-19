---
title: Bayesian Analysis of High Throughput Biological Measurement Data
authors:
  - name: Eric J. Ma
    affiliation: MIT
target_journal: nature_methods, pnas, elife, biostatistics, plos_comp_bio, plos_one
---

# Abstract

key points:
- simple framework for analysis
- accompanying software that loads CSV files
- instructions on how to use software

# Introduction

key points:
- HT screening data with duplicates or triplicates are common (cost is the biggest concern), but looking for `p < threshold` is prone to errors in inference due finding stuff that are statistically significant simply due to randomly extreme events (Kruschke). Triplicates may not necessarily sufficient for parameter estimation.
- Need: proper estimation of values of interest AND the uncertainty associated with it.
- Bayesian inference is a much more natural alternative, but it has generally been inaccessible to the general life science experimentalist; multiple comparisons are also not an issue (Kruschke).
- We do two things:
    - (1) extend Krushke's two-sample comparison method to fold changes (most common in HT analysis)
    - (2) provide open source software with UI to aid other researchers in conducting inference.

potential references:

1. Enhancing reproducibility in cancer drug screening: how do we move forward? http://www.ncbi.nlm.nih.gov/pubmed/25015668
1. Linear models and empirical bayes methods for assessing differential expression in microarray experiments. http://www.ncbi.nlm.nih.gov/pubmed/16646809
1. Empirical Bayesian analysis of paired high-throughput sequencing data with a beta-binomial distribution. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658937/
1. Bayesian Analysis of High-Throughput Quantitative Measurement of Protein-DNA Interactions http://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0026105

# Analysis Framework

key points:
- bayesian hierarchical model (BGM) of final readout
- what needs to be modelled, and what can be ignored? By setting things up such that plates are internally consistent, only need to do single replicates per plate, but do replicate plates on different experimental runs.
- error modelled as 95% HPD in posterior distribution

# Results

## Simulation Setup

key points:
- describe experimental setup:
  - batch effects are controlled for by having internal controls and standards
  - need figure
- describe BGM for a generic "fold change" HT assay.

## Modelled Error in estimate as function of number of replicates

key points:
- result: posterior distribution width on fold change estimate as a function of number of measurements

## Simulation with irregular distributions

may decide to put this in supplementary at the end, or not.

key points:
- result: posterior likelihood function still allows us to model variance nicely.

## Small-scale real-world measurement data.

key points:
- put analysis of polymerase assay data here; can even just be Vivian's replication data and that would be sufficient.

# Discussion

## "Precision is the goal"

key points:
- `n=3` + NHST has led to the proliferation of false positive results in the literature.
- `n=some_value` + bayesian can let us identify measurements that have a high degree of uncertainty/variation.
- decision rule is possible: check that 95% HPDs are non-overlapping. alternatively, have a pre-defined ROPE (Kruschke). emphasize: no free lunch.
- deciding whether something is significant should still be on the basis of "biological" significance, not "statistical" significance.
