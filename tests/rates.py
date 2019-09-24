"""Show frbpoppy matches analytical models and predict the event rates."""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np

from rates_toy import toy_rates
from rates_real import real_rates
from rates_simple import simple_rates
from rates_complex import complex_rates

MAKE = False
OBSERVE = False
PREDICTION = False
SIZE = 'small'
SURVEYS = ('palfa', 'htru', 'askap-fly')
ALPHAS = np.around(np.linspace(-0.2, -2.5, 7), decimals=2)
PLOT_COLS = 2

if PREDICTION:
    james = [-2.2-0.47, -2.2+0.47]  # James, Ekers et al. 2018


def plot(toy, simple, complex, real):
    # Use a nice font for axes
    plt.rc('text', usetex=True)
    if PLOT_COLS == 1:
        plt.rcParams["figure.figsize"] = (3.556, 3.556)
    else:
        plt.rcParams["figure.figsize"] = (5.75373, 3.556)


    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    cmap = plt.get_cmap('tab10')
    ax1.set_xlim((min(ALPHAS)+.1, max(ALPHAS)-.1))
    ax2.set_xlim((min(ALPHAS)+.1, max(ALPHAS)-.1))
    ax1.set_yscale('log', nonposy='mask')
    ax2.set_yscale('log', nonposy='mask')

    # Plot simple versus toy
    for i, surv in enumerate(SURVEYS):
        ax1.plot(ALPHAS, toy[surv], color=cmap(i), linestyle='dotted',
                 zorder=0)
        ax1.plot(ALPHAS, simple[surv], zorder=1)

    # Plot complex expectations
    for i, surv in enumerate(SURVEYS):
        ax2.plot(ALPHAS, complex[surv], color=cmap(i), linestyle='dashed',
                 zorder=1)

    # Plot prediction region
    if PREDICTION:
        top, bottom = ax2.get_ylim()
        ax2.set_ylim((top, bottom))
        left, right = james[0], james[1]
        x = [left, right, right, left]
        y = [top, top, bottom, bottom]
        ax2.fill(x, y, hatch='+', facecolor="none", edgecolor="k", linewidth=0.0,
                 alpha=0.25, zorder=0)

    # Plot real event rate boxes
    ma, mi = ax2.get_xlim()
    ma -= 0.05
    mi += 0.05
    size = 0.13
    z = 0
    for i, surv in enumerate(SURVEYS):

        central, min_r, max_r = real[surv]

        left = mi - size
        right = ma + size

        x, y = zip(*[(ma, max_r), (right, max_r), (right, min_r), (ma, min_r)])
        ax1.fill(x, y, color=cmap(i), zorder=z)
        ax1.plot([ma, right+0.08], [central, central], color=cmap(i), zorder=z)

        x, y = zip(*[(mi, max_r), (left, max_r), (left, min_r), (mi, min_r)])
        ax2.fill(x, y, color=cmap(i), zorder=z)
        ax2.plot([mi, left-0.08], [central, central], color=cmap(i), zorder=z)

        size -= 0.02
        z += 1

    # Plot layout options
    # Set up axes
    ax1.set_xlabel(r'$\alpha_{\mathrm{in}}$')
    ax1.invert_xaxis()
    ax1.set_ylabel('Events / htru')
    ax1.yaxis.set_ticks_position('left')
    ax1.title.set_text(r'\textit{Simple} populations')

    ax2.set_xlabel(r'$\alpha_{\mathrm{in}}$')
    ax2.invert_xaxis()
    ax2.yaxis.set_ticks_position('right')
    ax2.tick_params(labelright=False)
    ax2.title.set_text(r'\textit{Complex} populations')

    # Set up layout options
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)

    # Add legend elements
    elements = []
    for i, surv in enumerate(SURVEYS):
        c = cmap(i)
        line = Line2D([0], [0], color=c)
        label = surv
        elements.append((line, label))

    # Add gap in legend
    elements.append((Line2D([0], [0], color='white'), ''))

    # Add line styles
    n = 'analytical'
    elements.append((Line2D([0], [0], color='gray', linestyle='dotted'), n))
    elements.append((Line2D([0], [0], color='gray'), 'simple'))
    elements.append((Line2D([0], [0], color='gray', linestyle='dashed'),
                     'complex'))

    # Add gap in legend
    elements.append((Line2D([0], [0], color='white'), ''))

    elements.append((Patch(facecolor='gray', edgecolor='gray', alpha=0.6),
                     'real'))
    if PREDICTION:
        elements.append((Patch(facecolor='white', edgecolor='gray', hatch='+',
                               linewidth=0.1), 'prediction'))

    lines, labels = zip(*elements)
    plt.legend(lines, labels, bbox_to_anchor=(1.04, 0.5), loc="center left")

    plt.savefig('plots/rates.pdf', bbox_inches='tight')


def main():
    toy = toy_rates(surveys=SURVEYS,
                    alphas=ALPHAS)

    simple = simple_rates(make=MAKE,
                          observe=OBSERVE,
                          alphas=ALPHAS,
                          size=SIZE,
                          surveys=SURVEYS)

    complex = complex_rates(make=MAKE,
                            observe=OBSERVE,
                            alphas=ALPHAS,
                            size=SIZE,
                            surveys=SURVEYS)

    real = real_rates(surveys=SURVEYS)

    plot(toy, simple, complex, real)


if __name__ == '__main__':
    main()
