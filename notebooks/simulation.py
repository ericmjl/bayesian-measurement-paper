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

num_replicate_samples = np.arange(2, 21)

# Write one bash script for each simulation.
for n in num_replicate_samples:
    with open('sim_results/reps_{0}.sh'.format(n), 'w') as f:
        f.write(sge_header)
        f.write('cd ..\n')
        f.write('python model.py --n_reps={0} --n_sims=20\n'.format(n))


# Write master script
with open('sim_results/master.sh', 'w') as f:
    f.write(sge_header)
    for n in num_replicate_samples:
        f.write('qsub reps_{0}.sh\n'.format(n))
