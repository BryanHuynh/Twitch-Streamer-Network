import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
import powerlaw as pl
from pprint import pprint
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
from networkx.algorithms.community import k_clique_communities
import itertools

motifs = {
    # A -> B, B -> A, C -> B, C -> A, B -> C, C -> B
    'S13': (nx.DiGraph([ ('A','B'), ('B','A'), ('C','B'), ('C','A'), ('B','C'), ('C','B') ]))
}

def mcounter(gr, mo):
    # https://gist.github.com/tpoisot/8582648
    """Counts motifs in a directed graph
    :param gr: A ``DiGraph`` object
    :param mo: A ``dict`` of motifs to count
    :returns: A ``dict`` with the number of each motifs, with the same keys as ``mo``
    This function is actually rather simple. It will extract all 3-grams from
    the original graph, and look for isomorphisms in the motifs contained
    in a dictionary. The returned object is a ``dict`` with the number of
    times each motif was found.::
        >>> print mcounter(gr, mo)
        {'S1': 4, 'S3': 0, 'S2': 1, 'S5': 0, 'S4': 3}
    """
    #This function will take each possible subgraphs of gr of size 3, then
    #compare them to the mo dict using .subgraph() and is_isomorphic
    
    #This line simply creates a dictionary with 0 for all values, and the
    #motif names as keys

    mcount = dict(zip(mo.keys(), list(map(int, np.zeros(len(mo))))))
    nodes = gr.nodes()

    #We use iterools.product to have all combinations of three nodes in the
    #original graph. Then we filter combinations with non-unique nodes, because
    #the motifs do not account for self-consumption.

    triplets = list(itertools.product(*[nodes, nodes, nodes]))
    triplets = [trip for trip in triplets if len(list(set(trip))) == 3]
    triplets = map(list, map(np.sort, triplets))
    u_triplets = []
    [u_triplets.append(trip) for trip in triplets if not u_triplets.count(trip)]

    #The for each each of the triplets, we (i) take its subgraph, and compare
    #it to all fo the possible motifs

    for trip in u_triplets:
        sub_gr = gr.subgraph(trip)
        mot_match = map(lambda mot_id: nx.is_isomorphic(sub_gr, mo[mot_id]), motifs.keys())
        match_keys = [mo.keys()[i] for i in range(0, len(mo)) if mot_match[i]]
        if len(match_keys) == 1:
            mcount[match_keys[0]] += 1

    return mcount


if __name__ == '__main__':
    print("starting...")
    # read in the data
    df = pd.read_csv(sys.argv[1])
    _G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
    communities = list(greedy_modularity_communities(_G, 'Weight'))
    # get second biggest community
    max_com = communities[1]
    print(len(max_com))
    # make a subgraph with max_com 
    G = _G.subgraph(max_com)
    

    # find the number of matching motifs/subgraphs in the network
    motif_counts = mcounter(G, motifs)
    pprint(motif_counts)
    # plot the amount on a graph for each motif
    plt.bar(motifs.keys(), motif_counts.values())
    # save the graph
    plt.savefig('motifs.png')
    

    



    




    print("ending...")