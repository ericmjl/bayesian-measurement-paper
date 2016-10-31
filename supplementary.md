---
title: Supplementary Materials
---

# Analysis Framework

## Experimental Setup

If carefully considered, the problem of high throughput measurement at it essence is the measurement and estimation of a treatment's real-valued effect, relative to a standardized control. These are measured relative to a "blank" that should reliably exhibit an instrument signal at its lower limit of detection. Each treatment is statistically independent of every other treatment, as the effect of a treatment given to one well does not affect the outcome of treatment given to another well.

As a concrete example, consider the problem of systematically characterizing a protein mutant family. A standard design for this experiment might involve the following (Figure @fig:assay-scheme):

1. A blank well to define lower instrument limit of detection.
1. A negative control which forms a biological baseline measurement (e.g. reporter plasmid transfected without protein of interest), which may or may not return the same value as the blank.
1. A positive control that reliably returns a positive signal.
1. The suite of samples that require testing.

![Assay schematic. Yellow wells: samples. Green and blue: negative and positive controls (respectively). White wells: blanks.](./figures/assay-schematic.png){#fig:assay-scheme}

In this setup, the blanks and controls are measured on every single plate, providing a "ladder" against which the data can be compared; with many fold more replicate measurements than individual samples, an experimenter will have a more accurate estimate of their true means and variances. As the commonplace "relative luminescence units" do not allow for easy inter-comparison between experiments, we consider the following normalization procedure in order to achieve this.

Firstly, the blank is subtracted from every well, to standardize the samples.

Secondly, the samples `{i = 1, 2, 3, ... n, pc, nc, b}` and controls have their raw readings `r` normalized to the "true blank" `tb`. This allows every reading to be normalized to (i.e. divided by) the lower limit of detection, with the smallest value being 1. The fold relative to blank `µ` is given by Equation @eq:fold_blank, where `i` encompasses all samples, the controls, and the replicate blank. This normalized value is used for modelling the error in the fold changes. On each plate, each well gets at least a single replicate measurement; if there is space for duplicates, each replicate is considered an independent measurement of the activity relative to blank, rather than a value to be averaged.

$$ \mu_i = \frac{r_i}{r_{tb}} $$ {#eq:fold_blank}

Thirdly, with replicate plate measurements, there will be variation in the fold change relative to blank. Each computed fold change on the replicate plate is likewise considered an independent fold change measurement.

Using this experimental setup ensures that batch effects are accounted for in the measurement. Provided that there is little variation in the measurement of the blanks, every other sample's readings can be reliably normalized with uncertainty proportional to its true variation. The readings allow one to model the signal strength relative to noise.

## Bayesian Hierarchical Model

With this data on hand, we now consider the Bayesian hierarchical model. This model is an extension of the BEST model [@Kruschke:2013jy], in which more than one "treatment" is considered. As mentioned above, each treatment is considered to be independent of other treatments, for the application of a treatment (i.e. one mutation) does not affect the application of a treatment to another well.

We assume that the fold changes relative to blank are drawn from a uniform distribution from 10^-10^ to value `u` (+@eq:fold), essentially behaving as a flat positive-valued prior. The lower limit is set to an infinitesimally small value, allowing for uncertainty in the blank measurement. In order to use the data to estimate the upper limit of detection, we place a positive real-valued Exponential prior on it +@eq:upper.

$$ u \sim Exponential(\lambda=0.05) $$ {#eq:upper}

$$ \mu_{i} \sim Uniform(lower=l, upper=u) $$ {#eq:fold}

This places a positive real-valued prior on the master fold change distribution.

The errors `sigma` in fold change measurements are assumed to be drawn from a HalfCauchy distribution as recommended in [@Gelman:2006di], expressing our prior belief that the variance should be positively valued and low, but could also take high values.

$$ \sigma_{i} \sim HalfCauchy(\tau=5) $$ {#eq:sigma}

The data likelihood `L` is modelled as a Students T distribution, to account for potential outliers, with `nu` degrees of freedom as a prior.

$$ \nu \sim Exponential(\lambda=\frac{1}{30}) $$ {#eq:nu}

$$ L \sim StudentsT(\nu=\nu, \mu=\mu_{i}, \sigma=\sigma_{i}) $$ {#eq:likelihood}

Having modelled these variables, we can now deterministically compute fold changes and their full distributional uncertainty, given the data. Assuming the positive control were of interest as a "reference" standard, then the fold change `f` of each sample `s` relative to the positive control `pc` could be computed as:

$$ f_{s} = \frac{\mu_{s}}{\mu_{pc}} $$ {#eq:fold_change}

Z- and Z'-factors are used for assay evaluation and sample hit identification, relative to a baseline. Statistically, it is a measure of separation between two distributions, with possible values ranging from negative infinity to 1, with values closer to 1 indicating better separation, and hence better ability to resolve the two samples. With the posterior distribution of estimated fold changes and their variance, the Z- and Z'-factors and their distributional uncertainty may be computed using the formula below [@Zhang:1999fr]:

$$ Z = 1 - \frac{3\sigma_{s} + 3\sigma_{b}}{|\mu_{s} - \mu_{b}|} $$ {#eq:z_factor}
