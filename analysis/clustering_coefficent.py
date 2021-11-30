import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
from pprint import pprint

def draw_clustering_coefficent(G, title):
    N = len(G)
    L = G.size()
    clusterings = nx.clustering(G).values()
    # convert clustering to a numpy array
    
    # alternate form, maybe less convenient
    kmin = min(clusterings)
    kmax = max(clusterings)

    print(kmin, kmax)

    bin_edges = np.linspace((kmin), (kmax)+1)
    # histogram the data into these bins
    density, x = np.histogram(list(clusterings), bins=bin_edges, density=True)


    x = ((bin_edges[1:] + bin_edges[:-1])/2)
    
    fig = plt.figure(figsize=(10,10))
    
    plt.loglog(x, density, marker='o', linestyle='none')
    plt.xlabel(r"Clustering $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)



    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    fig.savefig("{}.png".format(title))
    return (x, density)


if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target')
    draw_clustering_coefficent(G, sys.argv[2])

    # plot clustering coefficent for G
    




