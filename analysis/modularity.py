import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
from networkx.algorithms.community import k_clique_communities
import sys
import pandas as pd
from pprint import pprint



def main():
    df = pd.read_csv('./nodes_with_top_games.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')
    communities = list(greedy_modularity_communities(G, 'Weight'))
    #pprint(communities)
    print("based on communtity detection: {}".format(nx_comm.modularity(G, communities)))
    communitiesBasedOnGame = generateCommunitiesBasedOnTopGames()
    print("Based on Top Game: {}".format(nx_comm.modularity(G, communitiesBasedOnGame, weight='Weight')))
    communitiesBasedOnLanguage = generateCommunitiesBasedOnLanguages()
    print("based on language: {}".format(nx_comm.modularity(G, communitiesBasedOnLanguage, weight='Weight')))
    communitiesBasedOnSharedLanguageAndGame = generateCommunitiesBasedOnSharedLanguageAndGame()
    print("based on shared language and game: {}".format(nx_comm.modularity(G, communitiesBasedOnSharedLanguageAndGame, weight='Weight')))


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

def generateCommunitiesBasedOnLanguages():
    df = pd.read_csv('./nodes_with_top_games.csv')
    communities = {}
    for index, row  in df.iterrows():
        if row['Source Language'] not in communities:
            communities[row['Source Language']] = []
        communities[row['Source Language']].append(row['Source']) if row['Source'] not in communities[row['Source Language']] else None

        if row['Target Language'] not in communities:
            communities[row['Target Language']] = []
        communities[row['Target Language']].append(row['Target']) if row['Target'] not in communities[row['Target Language']] else None

    communities_as_frozenset = []
    for key, value in communities.items():
        communities_as_frozenset.append(frozenset(value))

    return communities_as_frozenset

def generateCommunitiesBasedOnSharedLanguageAndGame():
    df = pd.read_csv('./nodes_with_top_games.csv')
    communities = {}
    for index, row  in df.iterrows():
        sourceLanguage = row['Source Language']
        targetLanguage = row['Target Language']
        sourceGame = row['Source Top Game']
        targetGame = row['Target Top Game']

        SourceLG = "{}|{}".format(sourceLanguage, sourceGame)
        TargetLG = "{}|{}".format(targetLanguage, targetGame)

        if SourceLG not in communities:
            communities[SourceLG] = []
        communities[SourceLG].append(row['Source']) if row['Source'] not in communities[SourceLG] else None
        if TargetLG not in communities:
            communities[TargetLG] = []
        communities[TargetLG].append(row['Target']) if row['Target'] not in communities[TargetLG] else None

    communities_as_frozenset = []
    for key, value in communities.items():
        communities_as_frozenset.append(frozenset(value))

    return communities_as_frozenset

if __name__ == '__main__':
    main()

