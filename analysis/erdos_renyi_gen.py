import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pprint import pprint

if __name__ == "__main__":
    # Read in the data
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    # get number of edges and nodes in G
    n_edges = G.number_of_edges()
    n_nodes = G.number_of_nodes()
    # generate 100 erdos Renyi graphs and save them to ER_models folder
    for i in range(100):
        ER = (nx.erdos_renyi_graph(n_nodes, n_edges/n_nodes))
        nx.write_edgelist(ER, 'ER_models/ER_model_' + str(i) + '.txt')

