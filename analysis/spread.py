from datetime import time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pandas as pd
from pprint import pprint
import smoothfit as sf
from tqdm import tqdm

timeline = None
node_status = pd.DataFrame(columns=['Node', 'Status', 'Timestamp'])
enable_timeline = True

def spread(G, Starting_nodes, spread_factor):
    if(enable_timeline):
        for node in Starting_nodes:
            node_status.loc[(node_status['Node'] == node), 'Timestamp'] = 0
            node_status.loc[(node_status['Node'] == node), 'Status'] = True

    #print("Starting nodes: ", Starting_nodes)
    return _spread(G, Starting_nodes, Starting_nodes, [], spread_factor)

def _spread(G, _influencers, _succeeded, _failed, spread_factor, timestamp=1):
    # go through the list of influencers
    # if there are no new influencers, return the succeeded list and failed list
    failed = _failed.copy()
    succeeded = _succeeded.copy()
    influencers = _influencers.copy()
    _ni = []
    
    for influencer in influencers:
    # find all their out going neighbours that are not in the succeeded list or failed list
        neighbours = [n[1] for n in G.out_edges(influencer)]
        # go through all neighbours in the failed list or succeeded list and remove them to the neighbours list
        for node in succeeded:
            if node in neighbours:
                neighbours.remove(node)

        for node in failed:
            if node in neighbours:
                neighbours.remove(node)
        # go through the neighbours
        for neighbour in neighbours:
            # try to activate them, if they succeed, add them to the succeeded list
            # if they fail, add them to the failed list
            # if add those who have succeeded to the next list of influencers
            if(activate(G, influencer, neighbour, spread_factor, timestamp)):
                #print("{} convince {}".format(influencer, neighbour), "influencer length: ", len(influencers))
                _ni.append(neighbour)
                succeeded.append(neighbour)
            else:
                failed.append(neighbour)

    #print("done spreading for current")
    # increment timestamp by one 
    timestamp += 1
    if(len(_ni) == 0):
        return succeeded, failed

    # repeat until the list of influencers is empty
    return _spread(G, _ni, succeeded, failed, spread_factor, timestamp)


def activate(G, influencer, target, spread_factor, timestamp):
    global timeline
    global enable_timeline
    # get the weight of the edge between the target and the influencer
    weight = G[influencer][target]['Weight']
    
    spread = spread_factor * 2
    if(weight < spread_factor):
        chance = (spread_factor - weight) / spread
    else:
        chance = (spread_factor + weight) / spread

    if(enable_timeline):
        timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Timestamp'] = timestamp
        node_status.loc[(node_status['Node'] == target), 'Timestamp'] = timestamp

    #print("influencer {0}, target {1}, chance {2}".format(influencer, target, chance))
    if(chance >= np.random.uniform(0,1)):
        # find Source and Target row in timeline and make assign their activation and timestamp
        if(enable_timeline):
            #print("influencer {0}, target {1}, timestamp {2}".format(influencer, target, timestamp))
            timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Activation'] = True
            node_status.loc[(node_status['Node'] == target), 'Status'] = True
        return True
    else:
        # find all in edges connected to target in G.
        # add the weight of G[influencer][target] to the weight of all edges connected to influencer
        # if the sum of weights is greater than spread_factor, return True, else return False
        in_edges = G.in_edges(target, data=True)
        for edge in in_edges:
            G[edge[0]][edge[1]]['Weight'] += weight
        # add influencer, target, false and Timestamp to the timeline
        if(enable_timeline):
            timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Activation'] = False
            node_status.loc[(node_status['Node'] == target), 'Status'] = False
        return False
    
std_weights = None    

def spread_data(G, start_size, data_function, average_size=5):
    data = data_function(G, start_size)
    # get time stamp of when it was activated and store it as meta data
    # which can be imported into gephi 
    top_nodes = []
    for nodes in data:
        top_nodes.append(nodes[0])
    # get standard deviation of all weights
    global std_weights
    if(std_weights is None):
        weights = []
        for edge in G.edges:
            weights.append(G[edge[0]][edge[1]]['Weight'])
        std_weights = np.std(weights)

    #std_weights = np.std(G.edges(data='Weight').values())
    #print("Standard Divation of weights: ", std_weights)
    average = 0
    for i in range(0, average_size):
        _G = G.copy()
        influenced, failed = spread(_G, top_nodes, std_weights)
        average += len(influenced) / len(G)
    #print("size of success: " + str(len(influenced)))
    #print("size of failed: " + str(len(failed)))
    #print("percentage: ", len(influenced) / len(G))
    return average / average_size

def get_random_nodes(G, size):
    nodes = []
    while(len(nodes) <= size):
        node = np.random.choice(G.nodes)
        if(node not in nodes):
            nodes.append(node)
    return nodes

degrees_data = None
def get_top_out_degree_nodes(G, size):
    global degrees_data
    if(degrees_data is None):
        degrees_data = nx.degree(G)
    print(sorted(degrees_data, key=lambda x: x[1], reverse=True)[:size])
    return sorted(degrees_data, key=lambda x: x[1], reverse=True)[:size]

betweenness_data = None
def get_top_betweenness_nodes(G, size):
    global betweenness_data
    if(betweenness_data == None):
        betweenness_data = nx.betweenness_centrality(G)
    print(sorted(betweenness_data.items(), key=lambda x: x[1], reverse=True)[:size])
    return sorted(betweenness_data.items(), key=lambda x: x[1], reverse=True)[:size]

closeness_data = None
def get_top_closeness_nodes(G, size):
    global closeness_data
    if(closeness_data == None):
        closeness_data = nx.closeness_centrality(G)
    return sorted(closeness_data.items(), key=lambda x: x[1], reverse=True)[:size]

eigenvector_data = None
def get_top_eigenvector_nodes(G, size):
    global eigenvector_data
    if(eigenvector_data == None):
        eigenvector_data = nx.eigenvector_centrality(G)
    return sorted(eigenvector_data.items(), key=lambda x: x[1], reverse=True)[:size]

def plot_fit_line(data, max_range, label):
    basis, coeffs = sf.fit1d(list(data.keys()), list(data.values()), 0, max_range, 1000, degree=1, lmbda=10)
    plt.plot(basis.mesh.p[0], coeffs[basis.nodal_dofs[0]], "-", label=label)


if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Usage: python3 spread.py <method> <max_size>")
        print("method: random, top_out_degree or top_betweenness or top_closeness or top_eigenvector or all")
        print("max_size: builds from 1 to the maximum size of starting active nodes")

        exit()
    timeline = pd.read_csv('./nodes_with_top_games.csv')
    # add new columns to timeline: activiation, timestamp
    if(enable_timeline):
        timeline['Activation'] = False
        timeline['Timestamp'] = -1
        # get all values from source and target
        source = timeline['Source'].values
        target = timeline['Target'].values
        # merge them and drop drop_duplicates
        nodes = np.concatenate((source, target), axis=None)
        nodes = np.unique(nodes)
        # add nodes to node_status
        node_status = pd.DataFrame(nodes, columns=['Node'])
        # add a column to node_status called 'Timestamp'
        node_status['Status'] = False
        node_status['Timestamp'] = -1

    G = nx.from_pandas_edgelist(timeline, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
    # if sys.argv[1] is random then use random nodes  
    # make all weights in graph 1

  
    average_size = 20
    if(enable_timeline):
        average_size = 1
    # make progress bars

    data = {}
    max_range = int(sys.argv[2])
    if(sys.argv[1] == "all"):
        data_r = {}
        data_td = {}
        data_tb = {}
        data_tc = {}
        data_te = {}

    pbar = tqdm(total=max_range)
    
    for i in range(max_range, max_range+1):
        if(sys.argv[1] == "random"):
            data[i] = spread_data(G, i, get_random_nodes, average_size=average_size)
        elif(sys.argv[1] == "top_out_degree"):
            data[i] = spread_data(G, i, get_top_out_degree_nodes, average_size=average_size)
        elif(sys.argv[1] == "top_betweenness"):
            data[i] = spread_data(G, i, get_top_betweenness_nodes, average_size=average_size)
        elif(sys.argv[1] == "top_closeness"):
            data[i] = spread_data(G, i, get_top_closeness_nodes, average_size=average_size)
        elif(sys.argv[1] == "top_eigenvector"):
            data[i] = spread_data(G, i, get_top_eigenvector_nodes, average_size=average_size)
        elif(sys.argv[1] == "all"):
            data_r[i] = spread_data(G, i, get_random_nodes, average_size=average_size)
            data_td[i] = spread_data(G, i, get_top_out_degree_nodes, average_size=average_size)
            data_tb[i] = spread_data(G, i, get_top_betweenness_nodes, average_size=average_size)
            data_tc[i] = spread_data(G, i, get_top_closeness_nodes, average_size=average_size)
            data_te[i] = spread_data(G, i, get_top_eigenvector_nodes, average_size=average_size)
        # make label of pbar data[i]
        if(sys.argv[1] != "all"):
            pbar.set_description("{}".format(data[i]))
        pbar.update(1)
    
    if(sys.argv[1] == "all"):
        plot_fit_line(data_r, max_range, "Random")
        plot_fit_line(data_td, max_range, "Top Out Degree")
        plot_fit_line(data_tb, max_range, "Top Betweenness")
        plot_fit_line(data_tc, max_range, "Top Closeness")
        plot_fit_line(data_te, max_range, "Top Eigenvector")
    else:
        plt.plot(list(data.keys()), list(data.values()), 'ro')
        basis, coeffs = sf.fit1d(list(data.keys()), list(data.values()), 0, max_range, 1000, degree=1, lmbda=100)
        plt.plot(basis.mesh.p[0], coeffs[basis.nodal_dofs[0]], "-", label="spread fit")

    plt.ylim(0, 1)
    plt.xlabel('Start Size')
    plt.ylabel('Percentage of Success')


    model = ""
    if(sys.argv[1] == "random"):
        plt.title('Random Node Spread')
        plt.savefig('spread_random_nodes{}.png'.format(model))
    elif(sys.argv[1] == "top_out_degree"):
        plt.title('Top Degree Node Spread')
        plt.savefig('spread_top_degree{}.png'.format(model))
    elif(sys.argv[1] == "top_betweenness"):
        plt.title('Top Betweenness Node Spread')
        plt.savefig('spread_top_betweenness{}.png'.format(model))
    elif(sys.argv[1] == "top_closeness"):
        plt.title('Top Closeness Node Spread')
        plt.savefig('spread_top_closeness{}.png'.format(model))
    elif(sys.argv[1] == "top_eigenvector"):
        plt.title('Top Eigenvector Node Spread')
        plt.savefig('spread_top_eigenvector{}.png'.format(model))
    elif(sys.argv[1] == "all"):
        # add legend
        plt.legend()
        plt.title('All Node Spread methods')
        plt.savefig('spread_all_nodes{}.png'.format(model))

    if(enable_timeline):
        timeline.to_csv('timeline.csv', index=False)
        node_status.rename(columns={'Node': 'Id'}, inplace=True)
        node_status.to_csv('node_status.csv', index=False)

 