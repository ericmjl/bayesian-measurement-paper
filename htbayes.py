import click
import pymc3 as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

@click.command()
@click.option('--filename', default='data.csv',
              help='File name of the data in CSV format.')
@click.option('--output_col', default='output',
              help='Name of column that contains data.')
@click.option('--sample_col', default='sample_name',
              help='Name of column that contains sample names.')
@click.option('--baseline_name', default='control',
              help='Name of positive control in sample names column.')
@click.option('--n_steps',  default=300000,
              help='Number of iterations for ADVI.')
def main(filename, sample_col, baseline_name, n_steps, output_col):
    data = load_data(filename)
    data, sample_names = convert_to_indices(data, sample_col)
    data = data.sort_values(by='indices')
    model = build_model(sample_names, data, baseline_name, output_col)
    trace = run_model(model, n_steps)
    plot_diagrams(trace, filename, baseline_name, output_col,
                  data, sample_col)


def load_data(filename):
    data = pd.read_csv(filename)
    return data


def convert_to_indices(data, sample_col):
    sample_names = dict()
    for i, name in enumerate(list(np.unique(data[sample_col].values))):
        print('Sample name {0} has the index {1}'.format(name, i))
        sample_names[name] = i
    data['indices'] = data[sample_col].apply(lambda x: sample_names[x])

    return data, sample_names


def build_model(sample_names, data, baseline_name, output_col):

    baseline_idx = sample_names[baseline_name]
    other_idx = sorted(list(set(data['indices']).difference([baseline_idx])))

    with pm.Model() as model:
        # Hyperpriors
        upper = pm.Exponential('upper', lam=0.05)
        nu = pm.Exponential('nu_minus_one', 1/29.) + 1

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
        like = pm.StudentT('like', nu=nu, mu=mu, sd=sig**-2,
                           observed=data[output_col])

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


def plot_diagrams(trace, filename, baseline_name, output_col,
                  data, sample_col):

    # Prep variables for below.
    sample_names = sorted(set(data[sample_col].values))
    prefix = filename.split('.')[0]

    # Make traceplot
    pm.traceplot(trace)
    plt.savefig('{0}-traceplot.pdf'.format(prefix), bbox_inches='tight')

    # Make forestplot
    pm.forestplot(trace, ylabels=sample_names, varnames=['fold'])
    plt.savefig('{0}-{1}-forestplot.pdf'.format(prefix, output_col),
                bbox_inches='tight')

    # Make forestplot of Z-factors
    pm.forestplot(trace, varnames=['z_factor'], xrange=(-1, 1), vline=0.5,
                  ylabels=sorted(set(sample_names)
                                 .difference([baseline_name])))
    plt.savefig('{0}-zfactor-forestplot.pdf'.format(prefix),
                bbox_inches='tight')

    # Make forestplot of fold changes
    pm.forestplot(trace, varnames=['fold_change'],
                  ylabels=sample_names)
    plt.savefig('{0}-fold_change-forestplot.pdf'.format(prefix),
                bbox_inches='tight')

    # Make summary plot #
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # 1. Get the lower error and upper errorbars for 95% HPD and IQR.
    lower, lower_q, upper_q, upper = np.percentile(trace['fold'],
                                                   [2.5, 25, 75, 97.5], axis=0)
    summary_stats = pd.DataFrame()
    summary_stats['mean'] = trace['fold'].mean(axis=0)
    err_low = summary_stats['mean'] - lower
    err_high = upper - summary_stats['mean']
    iqr_low = summary_stats['mean'] - lower_q
    iqr_high = upper_q - summary_stats['mean']

    # 2. Plot the swarmplot and errorbars.
    summary_stats['mean'].plot(rot=90, ls='', ax=ax, yerr=[err_low, err_high])
    summary_stats['mean'].plot(rot=90, ls='', ax=ax, yerr=[iqr_low, iqr_high],
                               elinewidth=4, color='red')
    sns.swarmplot(data=data, x=sample_col, y=output_col,
                  orient='v', ax=ax, alpha=0.5)
    plt.xticks(rotation='vertical')
    plt.ylabel(output_col)
    plt.savefig('{0}-summary_plot.pdf'.format(prefix), bbox_inches='tight')

    # Make summary dataframe.
    df_summary = pm.df_summary(trace)
    df_summary.to_csv('{0}-summary.csv'.format(prefix))


if __name__ == '__main__':
    main()
