import click
import pymc3 as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@click.command()
@click.option('--filename', default='data.csv',
              help='File name of the data in CSV format.')
@click.option('--column_name', default='sample_name',
              help='Name of column that contains sample names.')
@click.option('--baseline_name', default='control',
              help='Name of positive control in sample names column.')
@click.option('--n_steps',  default=300000,
              help='Number of iterations for ADVI.')
def main(filename, column_name, baseline_name, n_steps):
    data = load_data(filename)
    data, sample_names = convert_to_indices(data, column_name)
    model = build_model(sample_names, data, baseline_name)
    trace = run_model(model, n_steps)
    plot_diagrams(trace, filename, sample_names, baseline_name)


def load_data(filename):
    data = pd.read_csv(filename)
    return data


def convert_to_indices(data, column_name):
    sample_names = dict()
    for i, name in enumerate(list(np.unique(data[column_name].values))):
        print('Sample name {0} has the index {1}'.format(name, i))
        sample_names[name] = i
    data['indices'] = data[column_name].apply(lambda x: sample_names[x])

    return data, sample_names


def build_model(sample_names, data, baseline_name):

    baseline_idx = sample_names[baseline_name]
    other_idx = sorted(list(set(data['indices']).difference([baseline_idx])))

    with pm.Model() as model:
        # Hyperpriors
        upper = pm.Exponential('upper', lam=0.05)
        # lower = pm.Exponential('lower', lam=1)

        # "fold", which is the estimated fold change.
        fold = pm.Uniform('fold', lower=1E-10,
                          upper=upper, shape=len(sample_names))

        # Assume that data have heteroskedastic (i.e. variable) error but are
        # drawn from the same HalfCauchy distribution.
        sigma = pm.HalfCauchy('sigma', beta=1, shape=len(sample_names))

        # Model prediction
        mu = fold[data['indices']]
        sig = sigma[data['indices']]

        # Data likelihood
        like = pm.Normal('like', mu=mu, sd=sig,
                         observed=data['Normalized % GFP'])

        z_factor = pm.Deterministic('z_factor',
                                    (1 - ((sigma[other_idx] +
                                          sigma[baseline_idx]))
                                     / np.abs(fold[other_idx] -
                                              fold[baseline_idx])))

        fold_change = pm.Deterministic('fold_change',
                                       fold / fold[baseline_idx])

    return model

def run_model(model, n_steps=100000):
    with model:
        params = pm.variational.advi(n=n_steps)
        trace = pm.variational.sample_vp(params, draws=2000)

    return trace

def plot_diagrams(trace, filename, sample_names, baseline_name):
    prefix = filename.split('.')[0]
    pm.traceplot(trace)
    plt.savefig('{0}-traceplot.pdf'.format(prefix), bbox_inches='tight')

    pm.forestplot(trace, ylabels=sorted(sample_names), varnames=['fold'])
    plt.savefig('{0}-fold-forestplot.pdf'.format(prefix), bbox_inches='tight')

    pm.forestplot(trace, varnames=['z_factor'], xrange=(-1, 1), vline=0.5, ylabels=sorted(set(sample_names).difference([baseline_name])))
    plt.savefig('{0}-zfactor-forestplot.pdf'.format(prefix), bbox_inches='tight')

    pm.forestplot(trace, varnames=['fold_change'], ylabels=sorted(set(sample_names)))
    plt.savefig('{0}-fold_change-forestplot.pdf'.format(prefix), bbox_inches='tight')

    df_summary = pm.df_summary(trace)
    df_summary.to_csv('{0}-summary.csv'.format(prefix))


if __name__ == '__main__':
    main()
