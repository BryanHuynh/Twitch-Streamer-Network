import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':
    # Create a graph
    G = nx.Graph()

    # Add nodes
    G.add_node(1)
    G.add_nodes_from([2, 3])