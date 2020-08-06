"""Show how various parameters affect logNlogS."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import lines
from copy import deepcopy

from frbpoppy import CosmicPopulation, Survey, SurveyPopulation, hist
# from frbpoppy.population import unpickle

from tests.convenience import plot_aa_style, rel_path

SIZE = 1e4


class Flattening:

    def __init__(self, size):
        self.size = size
        self.zs = [0.01, 2, 6]
        self.survey = Survey('perfect')
        self.survey.set_beam('perfect')
        self.name = 'lognlogs_'
        self.plot()

    def gen_def_pop(self):
        self.default_pop = CosmicPopulation.simple(self.size)
        self.default_pop.name = self.name
        self.default_pop.generate()

    def survey_pop(self, pop):
        return SurveyPopulation(pop, self.survey)

    def gen_cos_pops(self):
        cosmo_pop = deepcopy(self.default_pop)
        pops = []
        for z in self.zs:
            cosmo_pop.set_dist(z_max=z)
            cosmo_pop.name = self.name + r'z$_{\text{max}}$=' + str(z)
            cosmo_pop.generate()
            surv_pop = self.survey_pop(cosmo_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)
        return pops

    def gen_lum_pops(self):
        lum_pop = deepcopy(self.default_pop)
        pops = []

        for z in [0.01, 6]:
            # Standard candles
            lum_pop.set_lum(model='constant', value=1e40)
            lum_pop.generate()
            lum_pop.name = self.name + f'std candle'
            surv_pop = self.survey_pop(lum_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

            # Powerlaw with slope
            power = -1
            lum_pop.set_lum(model='powerlaw', low=1e40, high=1e43, power=power)
            lum_pop.generate()
            lum_pop.name = self.name + f'li={power}'
            surv_pop = self.survey_pop(lum_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

            # Powerlaw with slope
            power = -2
            lum_pop.set_lum(model='powerlaw', low=1e40, high=1e43, power=power)
            lum_pop.generate()
            lum_pop.name = self.name + f'li={power}'
            surv_pop = self.survey_pop(lum_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

        return pops

    def gen_si_pops(self):
        si_pop = deepcopy(self.default_pop)
        pops = []

        for z in [0.01, 6]:
            si_pop.set_dist(z_max=z)
            for si in [-2, 0, 2]:
                si_pop.set_si(model='constant', value=si)
                si_pop.name = self.name + f'si={si}'
                si_pop.generate()
                surv_pop = self.survey_pop(si_pop)
                surv_pop.z_max = z
                pops.append(surv_pop)

        return pops

    def gen_w_pops(self):
        w_pop = deepcopy(self.default_pop)
        pops = []

        for z in [0.01, 6]:
            w_pop.set_dist(z_max=z)

            # Constant
            w_pop.set_w(model='constant', value=10)
            w_pop.generate()
            w_pop.name = self.name + f'constant'
            surv_pop = self.survey_pop(w_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

            # Normal
            w_pop.set_w(model='gauss', mean=10, std=10)
            w_pop.generate()
            w_pop.name = self.name + f'normal'
            surv_pop = self.survey_pop(w_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

            # Lognormal
            w_pop.set_w(model='lognormal', mean=10, std=10)
            w_pop.generate()
            w_pop.name = self.name + f'lognormal'
            surv_pop = self.survey_pop(w_pop)
            surv_pop.z_max = z
            pops.append(surv_pop)

        return pops

    def plot(self):

        plot_aa_style()
        plt.rcParams["figure.figsize"] = (5.75373, 5.75373)
        f, self.axes = plt.subplots(2, 2, sharey='row')

        self.linestyles = ['solid', 'dashed', 'dotted']
        self.colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
        self.lz = dict(zip(self.zs, self.linestyles))

        self.plot_cosmo()
        self.plot_lum()
        self.plot_si()
        self.plot_w()

        for ax in self.axes.flat:
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend()
            # Make the axis such that the diagonal is alpha=-1.5
            # ax.set_xlim(1, 10**(np.log10(self.size)/1.5))
            ax.set_xlim(1, 1e6)

        plt.tight_layout()
        plt.savefig(rel_path('plots/logn_logs_flattening.pdf'))

    def plot_cosmo(self):
        self.gen_def_pop()
        pops = self.gen_cos_pops()

        ax = self.axes[0, 0]
        ax.set_title('Cosmology')
        ax.set_ylabel(r'\#(${>}\text{S/N}$)')

        for i, pop in enumerate(pops):
            label = '_'.join(pop.name.split('_')[1:-1])
            ax.step(*self.calc_cum_hist(pop), where='mid',
                    label=rf'{label}', linestyle=self.linestyles[i],
                    color='grey')

    def plot_lum(self):
        pops = self.gen_lum_pops()

        # Plot details
        ax = self.axes[0, 1]
        ax.set_title('Luminosity')

        for i, pop in enumerate(pops):
            linestyle = self.lz[pop.z_max]
            colour = self.colours[int(i % (len(pops)/2))]
            label = '_'.join(pop.name.split('_')[1:-1])
            if i > (len(pops)/2 - 1):  # Turn off some line labels
                label = f'_{label}'
            ax.step(*self.calc_cum_hist(pop), where='mid',
                    label=rf'{label}', linestyle=linestyle,
                    color=colour)

    def plot_si(self):
        pops = self.gen_si_pops()

        # Plot details
        ax = self.axes[1, 0]
        ax.set_xlabel(r'S/N')
        ax.set_ylabel(r'\#(${>}\text{S/N}$)')
        ax.set_title('Spectral index')

        for i, pop in enumerate(pops):
            linestyle = self.lz[pop.z_max]
            colour = self.colours[int(i % (len(pops)/2))]
            label = '_'.join(pop.name.split('_')[1:-1])
            if i > (len(pops)/2 - 1):  # Turn off some line labels
                label = f'_{label}'
            ax.step(*self.calc_cum_hist(pop), where='mid',
                    label=rf'{label}', linestyle=linestyle,
                    color=colour)

    def plot_w(self):
        pops = self.gen_w_pops()

        # Plot details
        ax = self.axes[1, 1]
        ax.set_xlabel(r'S/N')
        ax.set_title('Pulse width')

        for i, pop in enumerate(pops):
            linestyle = self.lz[pop.z_max]
            colour = self.colours[int(i % (len(pops)/2))]
            label = '_'.join(pop.name.split('_')[1:-1])
            if i > (len(pops)/2 - 1):  # Turn off some line labels
                label = f'_{label}'
            ax.step(*self.calc_cum_hist(pop), where='mid',
                    label=rf'{label}', linestyle=linestyle,
                    color=colour)

    def calc_cum_hist(self, pop):
        # Bin up parameter in a cumulative bin
        edges, values = hist(pop.frbs.snr, bin_type='log')
        n_gt_s = np.cumsum(values[::-1])[::-1]

        # Normalise to S/N of 10^5
        log_diff = (np.log10(edges[0]) - np.log10(1e0))
        edges = 10**(np.log10(edges) - log_diff)

        return edges, n_gt_s


#
# for i, pops in enumerate(pops_to_plot):
#     for pop in pops:
#         # Bin up parameter in a cumulative bin
#         edges, values = hist(pop.frbs.snr, bin_type='log')
#         n_gt_s = np.cumsum(values[::-1])[::-1]
#
#         # Normalise to S/N of 10^5
#         log_diff = (np.log10(edges[0]) - np.log10(1e0))
#         edges = 10**(np.log10(edges) - log_diff)
#
#         # Set line type
#         linestyle = linestyles[0]
#         if hasattr(pop, 'z_max'):
#             try:
#                 ls_ix = self.zs.index(pop.z_max)
#             except ValueError:
#                 ls_ix = len(self.zs)
#             linestyle = linestyles[ls_ix]
#
#         # Create label
#         label = ' '.join(pop.name.split('_')[2:-1])
#         if 'z=' in label:
#             label = label.replace('z=', r'z$_{\text{max}}$=')
#
#         # Plot histogram
#         subplots[i].step(edges, n_gt_s, where='mid',
#                          label=rf'{label}', linestyle=linestyle)
#
#     # Figure out title
#     parameter = pop.name.split('_')[1]
#     if parameter == 'cosmo':
#         title = 'Cosmology'
#     elif parameter == 'lum':
#         title = 'Luminosity'
#     elif parameter == 'si':
#         title = 'Spectral Index'
#     elif parameter == 'w':
#         title = 'Pulse Width'
#     else:



if __name__ == '__main__':
    Flattening(SIZE)