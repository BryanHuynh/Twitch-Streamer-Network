import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pandas as pd
from pprint import pprint


def spread(G, Starting_nodes, spread_factor):
    return _spread(G, Starting_nodes, Starting_nodes, [], spread_factor)

def _spread(G, influencers, succeeded, failed, spread_factor):
    # go through the list of influencers
    # if there are no new influencers, return the succeeded list and failed list
    if(len(influencers) == 0):
        return succeeded, failed

    new_influencers = []
    for influencer in influencers:
    # find all their out going neighbours that are not in the succeeded list or failed list
        neighbours = [n[1] for n in G.out_edges(influencer)]
        # go through the neighbours
        for neighbour in neighbours:
            if(neighbour in succeeded or neighbour in failed):
                continue
            # try to activate them, if they succeed, add them to the succeeded list
            # if they fail, add them to the failed list
            # if add those who have succeeded to the next list of influencers
            if(activate(G, influencer, neighbour, spread_factor)):
                succeeded.append(neighbour)
                new_influencers.append(neighbour)
            else:
                failed.append(neighbour)
    # repeat until the list of influencers is empty
    return _spread(G, new_influencers, succeeded, failed, spread_factor)


def activate(G, influencer, target, spread_factor):
    # get the weight of the edge between the target and the influencer
    weight = G[influencer][target]['Weight']
    
    spread = spread_factor * 2
    if(weight < spread_factor):
        chance = (spread_factor - weight) / spread
    else:
        chance = (spread_factor + weight) / spread
    #print("influencer {0}, target {1}, chance {2}".format(influencer, target, chance))
    
    if(chance > np.random.uniform(0, 1)):
        return True
    
def spread_data(G, start_size):
    # compare  to randomly selected nodes
    data = sorted(G.degree, key=lambda x: x[1], reverse=True)[:start_size]
    
    # get time stamp of when it was activated and store it as meta data
    # which can be imported into gephi 
    top_nodes = []
    for nodes in data:
        top_nodes.append(nodes[0])

    # get standard deviation of all weights
    weights = []
    for edge in G.edges:
        weights.append(G[edge[0]][edge[1]]['Weight'])
    std_weights = np.std(weights)
    #std_weights = np.std(G.edges(data='Weight').values())
    #print("Standard Divation of weights: ", std_weights)
    average = 0
    for i in range(0,5):
        influenced, failed = spread(G, top_nodes, std_weights)
        average += len(influenced) / len(G)
    #print("size of success: " + str(len(influenced)))
    #print("size of failed: " + str(len(failed)))
    #print("percentage: ", len(influenced) / len(G))
    return average / 5

def spread_data_random(G, start_size):
    # compare  to randomly selected nodes
    data = []
    while(len(data) < start_size):
        data.append(np.random.choice(G.nodes))
    # get time stamp of when it was activated and store it as meta data
    # which can be imported into gephi 

    #print(top_nodes)
    # get standard deviation of all weights
    weights = []
    for edge in G.edges:
        weights.append(G[edge[0]][edge[1]]['Weight'])
    std_weights = np.std(weights)
    #print("Standard Divation of weights: ", std_weights)
    average = 0
    for i in range(0,5):
        influenced, failed = spread(G, data, std_weights)
        average += len(influenced) / len(G)
    #print("size of success: " + str(len(influenced)))
    #print("size of failed: " + str(len(failed)))
    #print("percentage: ", len(influenced) / len(G))
    return average / 5



if __name__ == "__main__":
    df = pd.read_csv('./nodes_with_top_games.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
    # if sys.argv[1] is random then use random nodes  
    if(len(sys.argv) > 1 and sys.argv[1] == "random"):
        print('running random node spread')
        rand_data = {}
        for i in range(1, 200):
            rand_data[i] = spread_data_random(G, i)
        plt.plot(list(rand_data.keys()), list(rand_data.values()))
        # draw best fit line
        # make y axis start a 0
        plt.ylim(0, 1)
        plt.xlabel('Start Size')
        plt.ylabel('Percentage of Success')
        plt.title('Random Node Spread')
        plt.savefig('random_spread_data.png')
    else:
        print('running top degree node spread')
        data = {}
        for i in range(1, 200):
            data[i] = spread_data(G, i)
        # plot the data with respect to i and data
        plt.plot(list(data.keys()), list(data.values()))
        # make y axis start a 0
        plt.ylim(0, 1)
        plt.xlabel('Start Size')
        plt.ylabel('Percentage of Success')
        plt.title('Top Degree Node Spread')
        plt.savefig('spread_data.png')

 