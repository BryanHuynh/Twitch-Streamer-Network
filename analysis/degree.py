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

    plt.loglog(x, density, marker='o', linestyle='none')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    #fit = pl.Fit(degrees, xmin=kmin, xmax=kmax)
    #fit.power_law.plot_pdf()

    fig.savefig("{}.png".format(title))
    return (x, density)

def degree_perserving_swap(graph, num_iterations):
  if num_iterations < 1:
    return -1
  # make a new empty directional graph
  G = nx.DiGraph()
  # make a dictionary where the keys are the nodes and the values are the degrees
  stubs = dict(graph.degree())
  # loop through every node in stubs
  for node in stubs:
    # for loop through the range of the degree of the node
    length = stubs[node]
    for i in range(0, length):
      # get a random node in stubs where the value is > 0 and not the node
      try:
        random_node = random.choice([x for x in stubs if stubs[x] > 0 and x != node])
      except:
        return degree_perserving_swap(graph, num_iterations - 1)
      # add an edge between the node and the random node
      G.add_edge(node, random_node)
      # decrement the degree of the random node
      stubs[random_node] -= 1
      # decrement the degree of the node
      stubs[node] -= 1
  # check that all stubs values are zeros
  if all(value != 0 for value in stubs.values()):
    return degree_perserving_swap(graph, num_iterations - 1)
  return G


if __name__ == "__main__":
    print('Starting')
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    x, density = draw_degree_distribution(G, "Degree_Distribution")
    null_model = degree_perserving_swap(G, 100)
    if(null_model != -1):
      draw_degree_distribution(null_model, "Degree_Distribution_Null_Model")
      # save null model to to_csv
      nx.write_edgelist(null_model, 'null_model.csv', data=True, delimiter=',')
    





 









