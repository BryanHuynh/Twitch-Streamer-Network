import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
import powerlaw as pl
from pprint import pprint
import random 
from collections import Counter
import itertools


def draw_degree_distribution(G, title):
    N = len(G)
    L = G.size()
    degrees = [G.degree(node) for node in G]

    kmin = min(degrees)
    kmax = max(degrees)

    print("Number of nodes: ", N)
    print("Number of edges: ", L)
    print()
    print("Average degree: ", 2*L/N)
    print("Average degree (alternate calculation)", np.mean(degrees))
    print()
    print("Minimum degree: ", kmin)
    print("Maximum degree: ", kmax)

    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax)+1, 400)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(10,10))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none', color='r')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # draw polynomial fit
    fit = np.polyfit(x, density, 1)
    fit_fn = np.poly1d(fit)
    plt.plot(x, fit_fn(x), '--k')

    fig.savefig("{}.png".format(title))
    return (x, density)


def draw_degree_distribution_with_null(G, G_null, title):
    N = len(G)
    L = G.size()
    degrees = [G.degree(node) for node in G]
    degrees_null = [G_null.degree(node) for node in G]

    kmin = min(degrees)
    kmax = max(degrees)

    print("Number of nodes: ", N)
    print("Number of edges: ", L)
    print()
    print("Average degree: ", 2*L/N)
    print("Average degree (alternate calculation)", np.mean(degrees))
    print()
    print("Minimum degree: ", kmin)
    print("Maximum degree: ", kmax)

    bin_edges = np.logspace(np.log10(kmin), np.log10(40)+1)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    density_null, _ = np.histogram(degrees_null, bins=bin_edges, density=True)

    fig = plt.figure(figsize=(10,10))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none', color='r', label='Twitch Streamers')
    plt.loglog(x, density_null, marker='o', linestyle='none', color='b', label='null model')
    plt.legend(loc="upper right")
    plt.title("Degree Distribution")
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    fit = pl.Fit(degrees, xmin=min(degrees), xmax=max(degrees))
    print('gamma fit: ', fit.power_law.alpha)
    fit.power_law.plot_pdf(color='red', linestyle='--', label='gamma fit')

    fig.savefig("{}.png".format(title))
    return (x, density)




if __name__ == "__main__":
    print('Starting')
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    x, density = draw_degree_distribution(G, "Degree_Distribution")
    df_null = pd.read_csv(sys.argv[2])
    G_null = nx.from_pandas_edgelist(df_null, source='Source', target='Target')
    x, density_null = draw_degree_distribution_with_null(G, G_null, "Degree_Distribution_with_null")
    





 









