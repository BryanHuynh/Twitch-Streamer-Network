import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
from pprint import pprint



def get_clustering_degree_dictionary(G):
    degree_dict = {}
    for node in G.nodes():
        degree = G.degree(node)
        if degree in degree_dict:
            degree_dict[degree].append(nx.clustering(G, node))
        else:
            degree_dict[degree] = [nx.clustering(G, node)]
    return degree_dict

def draw_clustering_coefficent_ER_models(title):
    null_model = pd.read_csv("./ER_models/erdos_renyi_graph_0.csv")
    # create graph for each null model, using first column and second columns as edges
    null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
    avg_null_clusterings = get_clustering_degree_dictionary(null_model_graph)
    for i in range(1,100):
        null_model = pd.read_csv("./ER_models/erdos_renyi_graph_{}.csv".format(i))
        # convert to graph
        null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
        null_model_clusterings = get_clustering_degree_dictionary(null_model_graph)
        # go through every key in average_null_clusterings and append to value of null_model_clusterings of same key
        for key in null_model_clusterings:
            if(key in avg_null_clusterings):
                # concat list_elements
                avg_null_clusterings[key] += null_model_clusterings[key]
            else:
                avg_null_clusterings[key] = null_model_clusterings[key]
    # go through every key in avg_null_clusterings and get the average of the values

    for key in avg_null_clusterings:
        avg_null_clusterings[key] = np.mean(avg_null_clusterings[key])/100

    # plot a graph of degree vs average clustering coefficient on a log scale. set x axis max to kmax
    # make y axis max be 1

    plt.figure(figsize=(10,10))

    plt.loglog(avg_null_clusterings.keys(), avg_null_clusterings.values(), 'ro')
    plt.xlabel('Degree')
    plt.ylabel('Average Clustering Coefficient')
    plt.ylim(0,1)
    # get line of best fit for the data
    x = np.array(list(avg_null_clusterings.keys()))
    y = np.array(list(avg_null_clusterings.values()))
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
    plt.savefig(title + ".png")

    return (x,y)

def draw_clustering_coefficent_null_models(title):
    null_model = pd.read_csv("./null_models/null_model_0.csv")
    # create graph for each null model, using first column and second columns as edges
    null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
    avg_null_clusterings = get_clustering_degree_dictionary(null_model_graph)
    for i in range(1,100):
        null_model = pd.read_csv("null_models/null_model_{}.csv".format(i))
        # convert to graph
        null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
        null_model_clusterings = get_clustering_degree_dictionary(null_model_graph)
        # go through every key in average_null_clusterings and append to value of null_model_clusterings of same key
        for key in null_model_clusterings:
            if(key in avg_null_clusterings):
                # concat list_elements
                avg_null_clusterings[key] += null_model_clusterings[key]
            else:
                avg_null_clusterings[key] = null_model_clusterings[key]
    # go through every key in avg_null_clusterings and get the average of the values

    for key in avg_null_clusterings:
        avg_null_clusterings[key] = np.mean(avg_null_clusterings[key])/100
    

    # plot a graph of degree vs average clustering coefficient on a log scale. set x axis max to kmax
    # make y axis max be 1

    plt.figure(figsize=(10,10))

    plt.loglog(avg_null_clusterings.keys(), avg_null_clusterings.values(), 'ro')
    plt.xlabel('Degree')
    plt.ylabel('Average Clustering Coefficient')
    plt.ylim(0,1)

    x = np.array(list(avg_null_clusterings.keys()))
    y = np.array(list(avg_null_clusterings.values()))
    # line of best fit degree 1
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
    plt.title(title)
    plt.savefig(title + ".png")
    return (x,y)
    



def draw_clustering_coefficent(G, title):
    N = len(G)
    L = G.size()
    # get max degree of graph
    # make a dictionary where the key is the degree and the values are the clustering coefficient of nodes with that degree
    degree_dict = {}
    for node in G.nodes():
        degree = G.degree(node)
        if degree in degree_dict:
            degree_dict[degree].append(nx.clustering(G, node))
        else:
            degree_dict[degree] = [nx.clustering(G, node)]

    # go through degree_dict and get the average clustering coefficient for each degree
    degree_avg_clustering = {}
    for degree in degree_dict:
        degree_avg_clustering[degree] = np.average(degree_dict[degree])

    # alternate form, maybe less convenient
    degrees = [G.degree(node) for node in G]

    kmin = min(degrees)
    kmax = max(degrees)
    print("kmin: {}".format(kmin))
    print("kmax: {}".format(kmax))

    # get average clustering coefficient of null model 
    null_x, null_y = draw_clustering_coefficent_null_models("Null_Model_clustering_coefficient")
    er_x, er_y = draw_clustering_coefficent_ER_models("ER_Model_clustering_coefficient")
    # plot a graph of degree vs average clustering coefficient on a log scale. set x axis max to kmax

    plt.figure(figsize=(10,10))
    plt.plot(np.unique(null_x), np.poly1d(np.polyfit(null_x, null_y, 1))(np.unique(null_x)), 'g', label='Null_Model_clustering_coefficient')
    plt.plot(np.unique(er_x), np.poly1d(np.polyfit(er_x, er_y, 1))(np.unique(er_x)), 'r', label='ER_Model_clustering_coefficient')
    plt.loglog(degree_avg_clustering.keys(), degree_avg_clustering.values(), 'bo', label='Average Clustering Coefficient')

    plt.xlabel('Degree')
    plt.ylabel('Average Clustering Coefficient')
    plt.style.use('classic')
    # show legend
    plt.legend(loc='best')

    plt.ylim(0,1)
    plt.xlim(kmin,kmax + 2)

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

   
    plt.title(title)
    plt.savefig(title + ".png")    


def get_average_clustering(G):
    N = len(G)
    L = G.size()
    clusterings = nx.average_clustering(G)
    print("Average clustering: {}".format(clusterings))

    # load in 100 null models from ./null_models/
    # calculate the clustering coefficient for each null model
    # then average them out
    # then plot the average clustering coefficient
    null_model = pd.read_csv("./null_models/null_model_0.csv")
    # create graph for each null model, using first column and second columns as edges
    null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
    avg_null_clusterings = nx.average_clustering(null_model_graph)
    for i in range(1,100):
        null_model = pd.read_csv("null_models/null_model_{}.csv".format(i))
        # convert to graph
        null_model_graph = nx.from_pandas_edgelist(null_model, source='Source', target='Target', create_using=nx.DiGraph())
        null_model_clusterings = nx.average_clustering(null_model_graph)
        # add every i element from null_model_clusterings to avg_null_clusterings
        avg_null_clusterings += null_model_clusterings
    avg_null_clusterings = avg_null_clusterings/100
    print("Average clustering of null models: {}".format(avg_null_clusterings))



if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Usage: {} <input_file> <output_file>".format(sys.argv[0]))
        sys.exit(1)
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', create_using=nx.DiGraph())
    #draw_clustering_coefficent_ER_models("ER_Model_clustering_coefficient")
    draw_clustering_coefficent(G, sys.argv[2])
    get_average_clustering(G)
    


    # plot clustering coefficent for G
    




