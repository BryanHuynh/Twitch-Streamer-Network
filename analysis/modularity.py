import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
from pprint import pprint



def main():
    df = pd.read_csv('./nodes_with_top_games.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    communities = list(greedy_modularity_communities(G, 'Weight'))
    #pprint(communities)
    print(nx_comm.modularity(G, communities))
    communitiesBasedOnGame = generateCommunitiesBasedOnTopGames()
    print(nx_comm.modularity(G, communitiesBasedOnGame, weight='Weight'))


def generateCommunitiesBasedOnTopGames():
    df = pd.read_csv('./nodes_with_top_games.csv')
    communities = {}
    for index, row  in df.iterrows():
        if row['Source Top Game'] not in communities:
            communities[row['Source Top Game']] = []
        communities[row['Source Top Game']].append(row['Source']) if row['Source'] not in communities[row['Source Top Game']] else None

        if row['Target Top Game'] not in communities:
            communities[row['Target Top Game']] = []
        communities[row['Target Top Game']].append(row['Target']) if row['Target'] not in communities[row['Target Top Game']] else None

    communities_as_frozenset = []
    for key, value in communities.items():
        communities_as_frozenset.append(frozenset(value))

    return communities_as_frozenset


if __name__ == '__main__':
    main()

