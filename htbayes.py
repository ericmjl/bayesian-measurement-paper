import click
import pymc3 as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging


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
    # data, sample_names = convert_to_indices(data, sample_col)
    # data = data.sort_values(by='indices')
    # model = build_model(sample_names, data, baseline_name, output_col)
    # trace = run_model(model, n_steps)
    # plot_diagrams(trace, filename, baseline_name, output_col,
    #               data, sample_col)
    b = BEST(data, sample_col, output_col, baseline_name)
    b.fit()
    b.plot_posterior()


def load_data(filename):
    data = pd.read_csv(filename)
    return data


class BEST(object):
    """BEST Model, based on Kruschke (2013).

    Parameters
    ----------
    data : pandas DataFrame
        A pandas dataframe which has the following data:
        - Each row is one replicate measurement.
        - There is a column that records the treatment name.
        - There is a column that records the measured value for that replicate.

    sample_col : str
        The name of the column containing sample names.

    output_col : str
        The name of the column containing values to estimate.

    baseline_name : str
        The name of the "control" or "baseline".

    Output
    ------
    model : PyMC3 model
        Returns the BEST model containing
    """
    def __init__(self, data, sample_col, output_col, baseline_name):
        super(BEST, self).__init__()
        self.data = data.sort_values(by=sample_col)
        self.sample_col = sample_col
        self.output_col = output_col
        self.baseline_name = baseline_name
        self.trace = None

        self._convert_to_indices()

    def _convert_to_indices(self):
        """
        Adds the "indices" column to self.data (DataFrame). This is necessary
        for the simplified model specification in the "fit" function below.
        """
        sample_names = dict()
        for i, name in enumerate(
                list(np.unique(self.data[self.sample_col].values))):
            logging.info('Sample name {0} has the index {1}'.format(name, i))
            sample_names[name] = i
        self.data['indices'] = self.data[self.sample_col].apply(
            lambda x: sample_names[x])

    def fit(self, n_steps=50000):
        """
        Creates a Bayesian Estimation model for replicate measurements of
        treatment(s) vs. control.

        Parameters
        ----------
        n_steps : int
            The number of steps to run ADVI.
        """

        sample_names = set(self.data[self.sample_col].values)

        with pm.Model() as model:
            # Hyperpriors
            # upper = pm.Exponential('upper', lam=0.05)
            nu = pm.Exponential('nu_minus_one', 1/29.) + 1

            # "fold", which is the estimated fold change.
            fold = pm.Flat('fold', shape=len(sample_names))

            # Assume that data have heteroskedastic (i.e. variable) error but
            # are drawn from the same HalfCauchy distribution.
            sigma = pm.HalfCauchy('sigma', beta=1, shape=len(sample_names))

            # Model prediction
            mu = fold[self.data['indices'].values]
            sig = sigma[self.data['indices'].values]

            # Data likelihood
            like = pm.StudentT('like', nu=nu, mu=mu, sd=sig**-2,
                               observed=self.data[self.output_col])

            # Sample from posterior
            v_params = pm.variational.advi(n=n_steps)
            start = pm.variational.sample_vp(v_params, 1)[0]
            cov = np.power(model.dict_to_array(v_params.stds), 2)
            step = pm.NUTS(scaling=cov, is_cov=True)
            logging.info('Starting MCMC sampling')
            trace = pm.sample(step=step, start=start, draws=2000)

        self.trace = trace
        self.model = model

    def plot_posterior(self, rotate_xticks=False):
        """
        Plots a swarm plot of the data overlaid on top of the 95% HPD and IQR
        of the posterior distribution.
        """

        # Make summary plot #
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # 1. Get the lower error and upper errorbars for 95% HPD and IQR.
        lower, low_q, upp_q, upper = np.percentile(self.trace['fold'][500:],
                                                   [2.5, 25, 75, 97.5],
                                                   axis=0)
        summary_stats = pd.DataFrame()
        summary_stats['mean'] = self.trace['fold'].mean(axis=0)
        err_low = summary_stats['mean'] - lower
        err_high = upper - summary_stats['mean']
        iqr_low = summary_stats['mean'] - low_q
        iqr_high = upp_q - summary_stats['mean']

        # 2. Plot the swarmplot and errorbars.
        summary_stats['mean'].plot(ls='', ax=ax,
                                   yerr=[err_low, err_high])
        summary_stats['mean'].plot(ls='', ax=ax,
                                   yerr=[iqr_low, iqr_high],
                                   elinewidth=4, color='red')
        sns.swarmplot(data=self.data, x=self.sample_col, y=self.output_col,
                      ax=ax, alpha=0.5)

        if rotate_xticks:
            logging.info('rotating xticks')
            plt.xticks(rotation='vertical')
        plt.ylabel(self.output_col)

        return fig, ax

    def plot_elbo(self):
        """
        Plots the ELBO values to help check for convergence.
        """
        fig = plt.figure()
        plt.plot(-np.log10(-self.params.elbo_vals))

        return fig

    def summary_stats(self):
        return pm.summary_df(self.trace)


if __name__ == '__main__':
    main()
