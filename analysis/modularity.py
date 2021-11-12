import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd



def main():
    edges_df = pd.read_csv('./Edges.csv')
    nodes_df = pd.read_csv('./Nodes.csv')
    G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target', edge_attr='Weight')
    communities = list(greedy_modularity_communities(G, 'Weight'))
    print(nx_comm.modularity(G, communities))

    G2 = nx.from_pandas_edgelist(nodes_df, source='Source', target='Target', edge_attr='Top Game')



if __name__ == '__main__':
    main()