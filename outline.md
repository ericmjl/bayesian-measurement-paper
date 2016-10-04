# Paper Target

eLife: Tools & Resources
PLoS Computational Biology:

# Paper Outline

What's the problems?

1. HT measurement: what is the right sample size? Commonly accepted practice is duplicates or triplicates, but is this enough to be accurate?
1. Statistical analysis involves t-tests + confidence intervals, but can we do better and gain "credibility" information as well?
1. Statistical parameters are computed (e.g. Z-scores), but is there sufficiently small uncertainty in the values to know whether it's reliably precise, given the data?

How do we address the problems?

1. Take a Bayesian approach, made accessible using probabilistic programming.
1. Developed a PGM that describes a variety of real and simulated experimental data.

What do we do/show?

1. Show that common practice of reporting mean ± SEM under-represents the uncertainty in values.
1. Show that we can gain distributional information on the credibility of measured and calculated parameters.
1. (oh-by-the-way) Deployed an accessible web tool for the scientific community.

Discussion:

1. Merits of Bayesian analysis: cite Kruschke's paper.
1. Merits of probabilistic programming: cite PyMC3 paper. (basically makes Bayesian methods accessible.)
1. We're making Bayesian analysis of measurement data accessible to the regular scientist.

# Figures

Figure 1: (a) Addresses "what is the right sample size". Simulated draws. (b) Addresses confidence intervals.

Figure 2: Addresses uncertainty in statistical parameters.
