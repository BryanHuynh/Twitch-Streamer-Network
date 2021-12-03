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


def draw_clustering_coefficent_with_null(G,G_null,title):
    N = len(G)
    L = G.size()
    clusterings = nx.clustering(G).values()
    clusterings_null = nx.clustering(G_null).values()

    # alternate form, maybe less convenient
    kmin_real = min(clusterings)
    kmax_real = max(clusterings)
    kmin_null = min(clusterings_null)
    kmax_null = max(clusterings_null)

    kmin = min(kmin_real, kmin_null)
    kmax = max(kmax_real, kmax_null)
    
    print(kmin, kmax)

    bin_edges = np.linspace((kmin), (kmax)+1)
    # histogram the data into these bins
    density, x = np.histogram(list(clusterings), bins=bin_edges, density=True)
    density_null, x_null = np.histogram(list(clusterings_null), bins=bin_edges, density=True)

    x = ((bin_edges[1:] + bin_edges[:-1])/2)

    
    fig = plt.figure(figsize=(10,10))
    
    plt.loglog(x, density, marker='o', linestyle='none',color='blue')
    plt.loglog(x, density_null, marker='o', linestyle='none',color='red')

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
    if (len(sys.argv) != 3):
        print("Usage: {} <input_file> <output_file>".format(sys.argv[0]))
        sys.exit(1)
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target')
    df_null = pd.read_csv('./null_model.csv')
    G_null = nx.from_pandas_edgelist(df_null, source='Source', target='Target')
    draw_clustering_coefficent_with_null(G,G_null,sys.argv[2])


    # plot clustering coefficent for G
    




