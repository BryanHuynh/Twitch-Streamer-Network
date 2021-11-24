import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
import powerlaw as pl
from pprint import pprint

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

    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax)+1, 40)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(10,10))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    fit = pl.Fit(degrees, xmin=kmin, xmax=kmax)
    fit.power_law.plot_pdf()

    fig.savefig("{}.png".format(title))
    return (x, density)

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    fig = plt.figure(figsize=(16,16))
    nx.draw_circular(G, node_size = 40)
    plt.savefig("Connections_circular.png")

    x, density = draw_degree_distribution(G, "Degree_Distribution")




 









