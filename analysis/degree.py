import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
import sys
import pandas as pd
from pprint import pprint
import random 
from collections import Counter
import itertools
from thinkstats2 import Pmf
import thinkplot
import smoothfit
import powerlaw as pl


def draw_degree_distribution(G, title):
    N = len(G)
    L = G.size()
    degrees = [G.degree(node) for node in G]

    kmin = min(degrees)
    kmax = max(degrees)

    print("Number of nodes: ", N)
    print("Number of edges: ", L)
    print()
    print("Average degree: ", 2*L/N)
    print("Average degree (alternate calculation)", np.mean(degrees))
    print()
    print("Minimum degree: ", kmin)
    print("Maximum degree: ", kmax)

    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax)+1, 400)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(10,10))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none', color='r')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # draw polynomial fit
    fit = pl.Fit(degrees, xmin=min(degrees), xmax=max(degrees))
    print('gamma fit: ', fit.power_law.alpha)
    fit.power_law.plot_pdf(color='red', linestyle='--', label='gamma fit')


    fig.savefig("{}.png".format(title))
    return (x, density)

def get_degree_random_model():
    df = pd.read_csv('./ER_models/erdos_renyi_graph_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target')
    degrees = [G.degree(node) for node in G]
    for i in range(1,100):
        df = pd.read_csv('./ER_models/erdos_renyi_graph_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target')
        degrees_random = [G.degree(node) for node in G]
        # concat lists of degrees
        degrees = degrees + degrees_random
    return degrees

def get_degrees_null_model():
    df = pd.read_csv('./null_models/null_model_0.csv')
    G = nx.from_pandas_edgelist(df, source='Source', target='Target')
    degrees = [G.degree(node) for node in G]
    for i in range(1,100):
        df = pd.read_csv('./null_models/null_model_{}.csv'.format(i))
        G = nx.from_pandas_edgelist(df, source='Source', target='Target')
        degrees_null = [G.degree(node) for node in G]
        # concat lists of degrees
        degrees = degrees + degrees_null
    return degrees

def draw_degree_distribution_with_null(Gclear, title):
    N = len(G)
    L = G.size()
    degrees = [G.degree(node) for node in G]
    degrees_null = get_degrees_null_model()
    degree_random = get_degree_random_model()

    kmax = max(degrees + degrees_null + degree_random)
    kmin = min(degrees + degrees_null + degree_random)


    print("Number of nodes: ", N)
    print("Number of edges: ", L)
    print()
    print("Average degree: ", 2*L/N)
    print("Average degree (alternate calculation)", np.mean(degrees))
    print()
    print("Minimum degree: ", kmin)
    print("Maximum degree: ", kmax)

    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax)+1, 300)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)
    density_null, _ = np.histogram(degrees_null, bins=bin_edges, density=True)
    density_random, _ = np.histogram(degree_random, bins=bin_edges, density=True)
    fig = plt.figure(figsize=(10,10))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none', color='r', label='Twitch Streamers')
    plt.loglog(x, density_null, marker='o', linestyle='none', color='b', label='null model')
    plt.loglog(x, density_random, marker='o', linestyle='none', color='g', label='Random Model')
    print(x)

    # get polyfit
    z = np.polyfit(x, density, 1)
    p = np.poly1d(z)
    plt.plot(x,density, '.', p(x), '-', color='r')




    
    plt.title("Degree Distribution")
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # draw polynomial fit





    plt.legend(loc="upper right")
    fig.savefig("{}.png".format(title))
    return (x, density)

def distrubution(G):
    degrees = [G.degree(node) for node in G]
    degrees_null = get_degrees_null_model()
    degrees_random = get_degree_random_model()

    figsize = (10,10)
    plt.figure(figsize=figsize)
    pmf_network = Pmf(degrees)
    pmf_null = Pmf(degrees_null)
    pmf_random = Pmf(degrees_random)
    # put on log log scales
    plt.loglog(list(pmf_network.GetDict().keys()), list(pmf_network.GetDict().values()), 'o', linestyle='none', color='b', label='Twitch Streamers')
    #plt.loglog(pmf_null.GetDict().keys(), pmf_null.GetDict().values(), 'ro')
    #plt.loglog(pmf_random.GetDict().keys(), pmf_random.GetDict().values(), 'go')

    # get best fit with smooth fit
    basis, coeffs = smoothfit.fit1d(list(pmf_network.GetDict().keys()), list(pmf_network.GetDict().values()), 0, max(degrees), 1000, degree=1, lmbda=100)
    plt.loglog(basis.mesh.p[0], coeffs[basis.nodal_dofs[0]], "-", label="network fit")

    basis, coeffs = smoothfit.fit1d(list(pmf_null.GetDict().keys()), list(pmf_null.GetDict().values()), 0, max(degrees_null), 1000, degree=1, lmbda=100)
    plt.loglog(basis.mesh.p[0], coeffs[basis.nodal_dofs[0]], "-.", label="null model fit", color='r')

    basis, coeffs = smoothfit.fit1d(list(pmf_random.GetDict().keys()), list(pmf_random.GetDict().values()), 0, max(degrees_random), 1000, degree=1, lmbda=1.0)
    plt.loglog(basis.mesh.p[0], coeffs[basis.nodal_dofs[0]], "-.", label="Erdos-Renyi fit", color='g')

    plt.ylim(1e-3, 1)
    plt.xlim(1, 250)

    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # get powerlaw alpha from degree distribution
    alpha_network = pl.Fit(degrees, xmin=min(degrees), xmax=max(degrees)).alpha
    alpha_null = pl.Fit(degrees_null, xmin=min(degrees_null), xmax=max(degrees_null)).alpha
    alpha_random = pl.Fit(degrees_random, xmin=min(degrees_random), xmax=max(degrees_random)).alpha
    print("Network alpha: ", alpha_network)
    print("Null model alpha: ", alpha_null)
    print("Random model alpha: ", alpha_random)

    plt.title("Degree Distribution")
    thinkplot.Save(root='degree_distribution',
                   xlabel='degree',
                   ylabel='probability')



if __name__ == "__main__":
    print('Starting')
    df = pd.read_csv(sys.argv[1])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    #x, density = draw_degree_distribution(G, "Degree_Distribution")
    #df_null = pd.read_csv(sys.argv[2])
    #G_null = nx.from_pandas_edgelist(df_null, source='Source', target='Target')
    #draw_degree_distribution_with_null(G, "Degree_Distribution_with_null")
    distrubution(G)






 









