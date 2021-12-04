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
  # loop through all nodes in graph 
  stubs = {}
  for node in graph.nodes():
    # get in and out degree of node
    in_degree = graph.in_degree(node)
    out_degree = graph.out_degree(node)
    stubs[node] = {'in':in_degree, 'out':out_degree}

  # loop through every node in stubs
  for node in stubs:
    # for loop through the range of the degree of the node
    length = stubs[node]['out']
    for i in range(0, length):
      # get a random node in stubs where the value is > 0 and not the node
      try:
        random_node = random.choice([x for x in stubs if stubs[x]['in'] > 0 and x != node])
      except:
        return degree_perserving_swap(graph, num_iterations - 1)
      # add an edge between the node and the random node
      G.add_edge(node, random_node)
      # decrement the degree of the random node
      stubs[random_node]['in'] -= 1
      # decrement the degree of the node
      stubs[node]['out'] -= 1

  # check that all stubs values in and out are zeros
  for node in stubs:
    if stubs[node]['in'] != 0 or stubs[node]['out'] != 0:
        return degree_perserving_swap(graph, num_iterations - 1)
  

  return G

if __name__ == "__main__":
    print('Starting')
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())

    for i in range(0, 100):
      print('Iteration: ' + str(i))
      null_model = degree_perserving_swap(G, 100)
      # convert graph to pandas dataframe
      null_model_df = pd.DataFrame(null_model.edges(data=True))
      # rename columns
      null_model_df.columns = ['Source', 'Target', 'Weight']
      # write to file
      null_model_df.to_csv('null_models/null_model_' + str(i) + '.csv', index=False)
    
