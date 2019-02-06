import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import config as CONF
import sys
from matplotlib.gridspec import GridSpec

"""
Reads datapts from the file data.pts and plots them in 2D plots.
This is useful for viewing the particle arangement from different directions.
It is also quite a bit faster than the 3D plots... """


def read_stats(file="stats.csv", numstats=7):

    statsdict = {}

    with open(file, 'r') as f:
        header, data = f.readlines()

        headers = header.strip().split(",")
        stats = data.strip().split(",")

        for n, typ in enumerate(headers[0:7]):
            statsdict[typ] = stats[n]

    return statsdict


def read_datapts(file="data.pts"):
    with open(file, 'r') as f:
        lines = f.readlines()
        n = len(lines)
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        for n, line in enumerate(lines):
            x[n], y[n], z[n] = line.strip().split("\t")
    return (x, y, z)


def savefig(name: str):
    filename = 'figures/{}.pdf'.format(name)
    plt.savefig(filename, bbox_inches='tight')


if __name__ == "__main__":
    # setup figures
    fig_width_pt = 455.2  # Get this from LaTeX using \showthe\columnwidth
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    #fig_width = 9
    fig_height = fig_width*golden_mean      # height in inches
    fig_size = [fig_width, fig_height]
    global_figsize = fig_size
    params = {'font.family': "Latin Modern Roman",
              'font.size': 10,
              'figure.titlesize': 10,
              'axes.titlesize': 10,
              'legend.fontsize': 10,
              'axes.labelsize': 10,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'savefig.bbox': "tight",
              'figure.figsize': fig_size, }
    plt.rcParams.update(params)

    # read datapts and stats
    data_x, data_y, data_z = read_datapts("data.pts")
    stats = read_stats("stats.csv")

    txtlines = ["Domain: {} x {} x {}".format(stats['sizex'], stats['sizey'], stats['sizez']),
                "Fill type: {}".format(stats['filltype']),
                "Fill: {}".format(stats['fill']),
                "Data points: {}".format(stats['ndatapts']), ]

    txt = "\n".join(txtlines)

    fig = plt.figure()
    gs = GridSpec(3, 3)
    axleft = fig.add_subplot(gs[:, 0])
    axcent = fig.add_subplot(gs[:, 1])
    axrtup = fig.add_subplot(gs[0:2, 2])
    axrtdn = fig.add_subplot(gs[2, 2])

    axes = [axleft, axcent, axrtup, axrtdn]

    size = 0.5

    axes[0].scatter(data_x, data_y, s=size, label="datapoints")
    axes[0].set_aspect('equal')
    axes[0].set_xlim((0, CONF.Lx))
    axes[0].set_ylim((0, CONF.Ly))
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')

    axes[1].scatter(data_z, data_y, s=size, label="datapoints")
    axes[1].set_aspect('equal')
    axes[1].set_xlim((0, CONF.Lz))
    axes[1].set_ylim((0, CONF.Ly))
    axes[1].set_xlabel('z')
    axes[1].set_ylabel('y')
    axes[1].get_yaxis().set_visible(False)

    axes[2].scatter(data_x, data_z, s=size, label="datapoints")
    axes[2].set_aspect('equal')
    axes[2].set_xlim((0, CONF.Lx))
    axes[2].set_ylim((0, CONF.Lz))
    axes[2].set_xlabel('x')
    axes[2].set_ylabel('z')
    axes[2].yaxis.tick_right()

    axes[3].set_aspect('equal')
    axes[3].get_xaxis().set_visible(False)
    axes[3].get_yaxis().set_visible(False)
    axes[3].text(-0.3, 0.5, txt, horizontalalignment='left',
                 verticalalignment='center', transform=axes[3].transAxes)
    axes[3].axis('off')

    fig.tight_layout()

    if len(sys.argv) > 1:
        plt.suptitle(" ".join([str(arg) for arg in sys.argv[1:]]))
    else:
        print("You may add a custom suptitle by passing arguments.")
        plt.suptitle("Data Point Distribution")

    #savefig("testcase_{}_{}".format(stats['filltype'], stats['fill'].split(".")[1][:2]))
    plt.show()
