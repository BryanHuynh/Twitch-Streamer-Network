import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pprint import pprint
import random 
from collections import Counter
import itertools

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

    for i in range(0, 100):
      null_model = degree_perserving_swap(G, 100)
      # convert graph to pandas dataframe
      null_model_df = pd.DataFrame(null_model.edges(data=True))
      # rename columns
      null_model_df.columns = ['Source', 'Target', 'Weight']
      # write to file
      null_model_df.to_csv('null_models/null_model_' + str(i) + '.csv', index=False)
    
