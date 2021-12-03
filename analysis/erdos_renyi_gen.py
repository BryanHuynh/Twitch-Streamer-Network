import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pprint import pprint
from statistics import mean
from random import choice
from random import sample

'''
    this was taken from reynoldsnip at 
    https://math.stackexchange.com/questions/3076596/generate-random-graphs-with-specific-mean-degree-and-mean-edge-weight
'''
class MyGraph(nx.Graph):
    def __init__(self, num_nodes, target_deg):
        super().__init__()
        self.num_nodes = num_nodes
        self.target_deg = target_deg
        self.add_nodes_from(range(self.num_nodes))
        while self.avg_deg() < self.target_deg:
            n1, n2 = sample(self.nodes(), 2)
            if(n1 == n2): 
                continue
            self.add_edge(n1, n2, weight=1)


    def avg_deg(self):
        return self.number_of_edges() * 2 / self.num_nodes



if __name__ == "__main__":
    # Read in the data
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    # get number of edges and nodes in G
    degrees = [d for n, d in G.degree()]
    average_degree = np.mean(degrees)
    n_nodes = G.number_of_nodes()
    print("Number of nodes: {}".format(n_nodes))
    print("Number of edges: {}".format(G.number_of_edges()))
    print("Average degree: {}".format(average_degree))
    # generate 100 erdos Renyi graphs that have the same number of nodes and same average degrees
    for i in range(100):
        print(i)
        G_er = MyGraph(n_nodes, average_degree)
        degrees_er = [d for n, d in G_er.degree()]
        average_degree_er = np.mean(degrees_er)
        # convert graph to pandas dataframe
        df_er = pd.DataFrame(G_er.edges(data=False))
        # change the name of the columns
        df_er.columns = ['Source', 'Target']
        # write the dataframe to a csv file
        df_er.to_csv('./ER_models/erdos_renyi_graph_{}.csv'.format(i), index=False)

