import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import powerlaw as pl
from collections import defaultdict
import pandas as pd

almost_black = '#262626'
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = almost_black
plt.rcParams['text.color'] = almost_black
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['axes.labelsize'] = 12


def despine():
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')



def plot_deg_dist_and_fit(G, bins):
    deg = [val for (node, val) in G.degree()]
    kmin, kmax = min(deg), max(deg)
    be = np.logspace(np.log10(kmin), np.log10(kmax), bins) # logarithms of bin edges
    logbe = np.log10(be)
    # "x" values should be midway through each bin (in log space)
    x = 10**((logbe[1:] + logbe[:-1])/2)
    # plot empirical data
    p, _ = np.histogram(deg, bins=be, density=True)
    plt.loglog(x, p, linestyle='none', marker='o', alpha=0.65,
               markeredgecolor='none', label="N = {0}".format(len(G)))
    # plot theoretical fit
    fit = pl.Fit(deg, xmin=min(deg), xmax=max(deg))
    print('gamma= ',fit.power_law.alpha)
    fit.power_law.plot_pdf()
    plt.savefig('BA.png')

def main(): 
    df = pd.read_csv('./nodes_with_top_games.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    N = len(G)

    #generate barabasi albert graph 
    graph = nx.barabasi_albert_graph(N,1)

    special_sizes = [10,50,N]
    bins = dict(zip(special_sizes, [10,20,30]))

    ax = plt.subplot(111)
    if N in special_sizes:
        plot_deg_dist_and_fit(graph,bins[N])

    plt.legend(frameon=False, numpoints=1)
    plt.xlabel(r"degree, $k$")
    plt.ylabel(r"$P(k)$")
    despine()
    plot.savefig('BA.png')



if __name__ == '__main__':
    main()
