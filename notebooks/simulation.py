"""
Author: Eric J. Ma
Purpose: This is the master controller script that runs all of the simulations on SGE.
"""

import os
import sys
import numpy as np

# First part: simulations for fraction of samples that have true mean inside
# estimated HPD, and how that varies with the number of replicate samples.

sge_header = """
#!/bin/sh
#$ -S /bin/sh
#$ -cwd
#$ -V
#$ -m e
#$ -M ericmjl@mit.edu
#$ -pe whole_nodes 1
#############################################


"""

# Write master script
with open('sim_results/master.sh', 'w') as f:
    f.write(sge_header)
    f.write('python model.py --max_n_reps=21 --n_sims=20\n')
