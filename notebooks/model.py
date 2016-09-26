import numpy as np
import numpy.random as npr
import pymc3 as pm
import matplotlib.pyplot as plt
import click
import pickle as pkl

@click.command()
@click.option('--max_n_reps', default=2, help="Number of replicate samples.")
@click.option('--n_sims', default=10, help="Number of replicate simulations.")
def run_fract_correct_simulations(max_n_reps, n_sims):
    """
    n = the number of replicates samples for each.
    n_simulations = the number of replicate simulations to run
    """
    n_reps_data = list()
    fraction_correct_data = list()
    n_genotypes = 100
    for n_reps in range(max_n_reps):
        for sim in range(n_sims):
            print(' n_reps: {0},\n simulation number: {1}\n'.format(n_reps, sim))
            sim_data = make_simulated_data(n_genotypes=n_genotypes, n_reps=n_reps)
            data, indices, num_measurements, means, sds = sim_data
            print(indices)
            model = make_model(n_genotypes, data, indices)
            trace = sample_model(model, n_genotypes)

            lower, upper = np.percentile(trace['fold'], [2.5, 97.5], axis=0)
            frac_correct = sum((means > lower) * (means < upper)) / len(means)

            fraction_correct_data.append(frac_correct)
            n_reps_data.append(n_reps)

    with open('sim_results/{0}_reps.pkl'.format(n_reps), 'wb') as f:
        pkl.dump((n_reps_data, fraction_correct_data), f)

def plot_forestplots(trace):
    fig = plt.figure()
    pm.forestplot(trace, vline=1, varnames=['fold'])

    fig = plt.figure()
    pm.forestplot(trace, varnames=['z_factor', 'zp_factor'], xrange=(-1, 1), vline=0.5)

    fig = plt.figure()
    pm.forestplot(trace, varnames=['sigma'])

    plt.figure()
    pm.forestplot(trace, varnames=['fold_changes'], vline=1)


def sample_model(model, n_genotypes):
    with model:
        if n_genotypes <= 10:
            n_steps = 200000
        elif n_genotypes > 10:
            n_steps = 500000
        params = pm.variational.advi(n=n_steps)
        trace = pm.variational.sample_vp(params, draws=2000)

    return trace

def make_model(n_genotypes, data, indices):
    with pm.Model() as model:
        # Hyperpriors
        upper = pm.Exponential('upper', lam=0.05)
        # lower = pm.Exponential('lower', lam=1)

        # "fold", which is the estimated fold change.
        fold = pm.Uniform('fold', lower=1E-10, upper=upper, shape=n_genotypes+2)

        # Assume that data have heteroskedastic (i.e. variable) error but are drawn from the same distribution
        # sigma = pm.Gamma('sigma', alpha=1, beta=1, shape=n_genotypes+2)
        sigma = pm.HalfCauchy('sigma', beta=1, shape=n_genotypes+2)

        # Model prediction
        mu = fold[indices]
        sig = sigma[indices]

        # Data likelihood
        like = pm.Normal('like', mu=mu, sd=sig, observed=data)

        # Compute Z-factors relative to positive ctrl.
        z_factor = pm.Deterministic('z_factor', 1 - (3 * sigma[:-1] + 3 * sigma[-1]) / np.abs(fold[:-1] - fold[-1]))

        # Compute Z-prime factor between negative and positive control.
        zp_factor = pm.Deterministic('zp_factor', 1 - (3 * sigma[-2] + 3 * sigma[-1]) / np.abs(fold[-2] - fold[-1]))

        # Compute fold changes
        fold_changes = pm.Deterministic('fold_changes', fold[:-2] / fold[-1])


    return model

def make_simulated_data(n_reps, n_genotypes):
    means = npr.randint(low=10, high=100, size=n_genotypes)
    means = means * (means > 0)  # negative activities are not captured
    sds = npr.random(size=n_genotypes) * 10
    num_measurements = npr.randint(low=n_reps, high=n_reps+1, size=n_genotypes)

    # Create simulated data.
    data = []
    indices = []

    for i in range(n_genotypes):
        n = num_measurements[i]
        mean = means[i]
        sd = sds[i]

        measurements = npr.normal(loc=mean, scale=sd, size=n)
        # print(measurements)
        measurements = measurements * (measurements > 0)
        # print(measurements)

        data.extend(measurements.tolist())
        indices.extend([i] * n)

    # Add baseline measurements (bl_measures)
    n_bl_measures = n_reps
    bl_measures = npr.normal(loc=1.0, scale=0.1, size=n_bl_measures)
    bl_measures = bl_measures * (bl_measures > 0)
    data.extend(bl_measures)
    indices.extend([n_genotypes] * n_bl_measures)
    num_measurements = np.append(num_measurements, n_bl_measures)
    means = np.append(means, bl_measures.mean())
    sds = np.append(sds, bl_measures.std())

    # Add pos_ctrl measurements (pc_measures)
    n_pc_measures = n_reps
    pc_measures = npr.normal(loc=20.0, scale=1, size=n_pc_measures)
    pc_measures = pc_measures * (pc_measures > 0)
    data.extend(pc_measures)
    indices.extend([n_genotypes + 1] * n_pc_measures)
    num_measurements = np.append(num_measurements, n_pc_measures)
    means = np.append(means, pc_measures.mean())
    sds = np.append(sds, pc_measures.std())

    # convert indices to a numpy array
    indices = np.array(indices)

    return data, indices, num_measurements, means, sds,

if __name__ == '__main__':
    run_fract_correct_simulations()
