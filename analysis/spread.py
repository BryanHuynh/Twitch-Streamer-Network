import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pandas as pd
from pprint import pprint

timeline = None
node_status = pd.DataFrame(columns=['Node', 'Status', 'Timestamp'])

def spread(G, Starting_nodes, spread_factor):
    for node in Starting_nodes:
        node_status.loc[(node_status['Node'] == node), 'Timestamp'] = 0
        node_status.loc[(node_status['Node'] == node), 'Status'] = True

    print("Starting nodes: ", Starting_nodes)
    return _spread(G, Starting_nodes, Starting_nodes, [], spread_factor)

def _spread(G, _influencers, _succeeded, _failed, spread_factor, timestamp=1):
    print("timestamp: ", timestamp)
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
                print("{} convince {}".format(influencer, neighbour), "influencer length: ", len(influencers))
                _ni.append(neighbour)
                succeeded.append(neighbour)
            else:
                print("{} failed to convince {}".format(influencer, neighbour))
                failed.append(neighbour)

    print("done spreading for current")
    # increment timestamp by one 
    timestamp += 1
    if(len(_ni) == 0):
        return succeeded, failed

    # repeat until the list of influencers is empty
    return _spread(G, _ni, succeeded, failed, spread_factor, timestamp)


def activate(G, influencer, target, spread_factor, timestamp):
    global timeline
    # get the weight of the edge between the target and the influencer
    weight = G[influencer][target]['Weight']
    
    spread = spread_factor * 2
    if(weight < spread_factor):
        chance = (spread_factor - weight) / spread
    else:
        chance = (spread_factor + weight) / spread
    #print("influencer {0}, target {1}, chance {2}".format(influencer, target, chance))
    if(chance >= np.random.uniform(0,1)):
        # find Source and Target row in timeline and make assign their activation and timestamp
        #print("influencer {0}, target {1}, timestamp {2}".format(influencer, target, timestamp))
        timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Activation'] = True
        timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Timestamp'] = timestamp
        node_status.loc[(node_status['Node'] == target), 'Timestamp'] = timestamp
        node_status.loc[(node_status['Node'] == target), 'Status'] = True
        return True
    else:
        # add influencer, target, false and Timestamp to the timeline
        timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Activation'] = False
        timeline.loc[(timeline['Source'] == influencer) & (timeline['Target'] == target), 'Timestamp'] = timestamp
        node_status.loc[(node_status['Node'] == target), 'Timestamp'] = timestamp
        node_status.loc[(node_status['Node'] == target), 'Status'] = False
        return False
    
def spread_data(G, start_size, size = 1):
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
    #for i in range(0, size):
    influenced, failed = spread(G, top_nodes, std_weights)
    average += len(influenced) / len(G)
    #print("size of success: " + str(len(influenced)))
    #print("size of failed: " + str(len(failed)))
    #print("percentage: ", len(influenced) / len(G))
    return average / size

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
    timeline = pd.read_csv('./nodes_with_top_games.csv')
    # add new columns to timeline: activiation, timestamp
    timeline['Activation'] = False
    timeline['Timestamp'] = 15

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
    node_status['Timestamp'] = 15
    G = nx.from_pandas_edgelist(timeline, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
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
        '''
        for i in range(1, 200):
            data[i] = spread_data(G, i)
        '''
        
        data[0] = spread_data(G, 5)
        # plot the data with respect to i and data
        plt.plot(list(data.keys()), list(data.values()))
        # make y axis start a 0
        plt.ylim(0, 1)
        plt.xlabel('Start Size')
        plt.ylabel('Percentage of Success')
        plt.title('Top Degree Node Spread')
        plt.savefig('spread_data.png')
        # save timeline to csv file
        timeline.to_csv('timeline.csv', index=False)
        node_status.rename(columns={'Node': 'Id'}, inplace=True)
        node_status.to_csv('node_status.csv', index=False)

 