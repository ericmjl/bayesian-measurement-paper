---
title: Simple Bayesian Analysis of High Throughput Biological Measurement Data
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
- HT screening data are necessary for systematically interrogating biology. Statistical analysis of HT data is most commonly done with NHST, with multiple hypothesis testing corrections applied. Interpretation of the p-values returned depends on the intent of the experimenter (Kruschke), and the interpretation of the confidence intervals is contrived and unnatural.
- Posterior distributions computed based on Bayesian approaches provide a much more natural interpretation than frequentist. Because HT assays are at their essence 'measurements relative to a standard control', we can extend Kruschke's two-sample framework to multiple samples, and obtain proper estimation of values of interest *and* the uncertainty associated with it.
- Bayesian inference is a much more natural alternative, but it has generally been inaccessible to the general life science experimentalist; multiple comparisons are also not an issue (Kruschke).
- We do two things:
    - (1) extend Krushke's two-sample comparison method to fold changes (most common in HT analysis)
    - (2) provide open source software with UI to aid other researchers in conducting inference.

potential references:

1. Enhancing reproducibility in cancer drug screening: how do we move forward? http://www.ncbi.nlm.nih.gov/pubmed/25015668
1. Linear models and empirical bayes methods for assessing differential expression in microarray experiments. http://www.ncbi.nlm.nih.gov/pubmed/16646809
1. Empirical Bayesian analysis of paired high-throughput sequencing data with a beta-binomial distribution. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3658937/
1. Bayesian Analysis of High-Throughput Quantitative Measurement of Protein-DNA Interactions http://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0026105

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

We present with justifications a simple experimental setup for high throughput assays, a flat file data format for storing the fold change calculations, and a Bayesian analysis framework for modelling uncertainty in calculated fold changes.

To provide a concrete example, consider a high throughput assay measuring the drug resistance value of a family of protein variants relative to a standardized control. In a 96-well format experiment, a researcher would at the minimum have to include a "blank" well and one well for the reference control. Traditionally, the plate is set up such that each mutant (including the blank and reference) is measured in triplicate on one plate; this captures biological variation within a single plate. In a puzzling move, the data are normalized by subtracting the mean of the blanks' values from every well (by definition resulting in at least one negatively-valued blanks well if there is variation in the measured blanks). The mean of each triplicate sample is then divided by the mean of the references, thereby making the assumption that the reference sample is properly measured. This forms the fold change calculation for one plate, apparently controlling for biological variation. This procedure is replicated two more times, and the mean and variance of the three fold changes calculated are taken to be the data to be published. This two-step calculation procedure is supposed to account for biological and technical variation hierarchically, but much data are lost in averaging the computed means from triplicate measurements in one plate. In an even more puzzling move, some researchers choose to pool all 9 measurements together after 'eyeballing' the data to determine that the values are roughly the same, discarding altogether the need to reference for technical variation resulting from batch effects.

We propose here a small variation on the experimental setup that simultaneously incorporates technical and biological noise into the data, and provides a much more natural path to data interpretation. Here, each plate only contains a single measurement per sample and the blank, except for the reference, which is cloned. The singly-measured blank value is subtracted from each well, resulting in a blank well that, by definition, is and should be zero-valued. The reference and every sample is then divided by the cloned reference. This constitutes a single measurement of the fold change. This same set of samples is then replicate measured in separate experimental runs, as many times as the experimenter requires. With a new set of samples, keeping the same blank and reference control present allows for many replicate measurements of the reference control, leading to progressively precise estimates of the values relative to the control.

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
