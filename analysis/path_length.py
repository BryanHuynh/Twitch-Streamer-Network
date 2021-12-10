import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm

import sys
import pandas as pd
from pprint import pprint

def null_models_average_path():
    df = pd.read_csv('./null_models/null_model_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None, create_using=nx.DiGraph())
    avg_length = nx.average_shortest_path_length(G)
    for i in range(1,100):
        df = pd.read_csv('./null_models/null_model_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None, create_using=nx.DiGraph())
        avg_length += nx.average_shortest_path_length(G)
    avg_length = avg_length / 100
    print('average length of null model: {}'.format(avg_length))

def average_connected_component_size():
    df = pd.read_csv('./null_models/null_model_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None)
    avg_size = nx.number_connected_components(G)
    for i in range(1,100):
        df = pd.read_csv('./null_models/null_model_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None)
        avg_size += nx.number_connected_components(G)
    avg_size = avg_size / 100
    print('average number of connected components of null model: {}'.format(avg_size))


def average_connected_component_size_random_model():
    df = pd.read_csv('./ER_models/erdos_renyi_graph_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None)
    avg_size = nx.number_connected_components(G)
    for i in range(1,100):
        df = pd.read_csv('./ER_models/erdos_renyi_graph_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None)
        avg_size += nx.number_connected_components(G)
    avg_size = avg_size / 100
    print('average number of connected components of random model: {}'.format(avg_size))

def random_model_average_path():
    df = pd.read_csv('./ER_models/erdos_renyi_graph_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None, create_using=nx.DiGraph())
    avg_length = nx.average_shortest_path_length(G)
    for i in range(1,100):
        df = pd.read_csv('./ER_models/erdos_renyi_graph_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr=None, create_using=nx.DiGraph())
        avg_length += nx.average_shortest_path_length(G)
    avg_length = avg_length / 100
    print('average length of random model: {}'.format(avg_length))

if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
    print("average shortest path length: {0}".format(nx.average_shortest_path_length(G)))
    random_model_average_path()
    null_models_average_path()
    average_connected_component_size()
    average_connected_component_size_random_model()

    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    print("average number of connected components of real model: {0}".format(nx.number_connected_components(G)))