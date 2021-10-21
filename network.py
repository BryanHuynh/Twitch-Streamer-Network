import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
import sys
from tqdm import tqdm


def changeDefaultMPLStyle():
    mpl.rc('xtick', labelsize=14, color="#222222") 
    mpl.rc('ytick', labelsize=14, color="#222222") 
    mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
    mpl.rc('font', size=16)
    mpl.rc('xtick.major', size=6, width=1)
    mpl.rc('xtick.minor', size=3, width=1)
    mpl.rc('ytick.major', size=6, width=1)
    mpl.rc('ytick.minor', size=3, width=1)
    mpl.rc('axes', linewidth=1, edgecolor="#222222", labelcolor="#222222")
    mpl.rc('text', usetex=False, color="#222222")

def loadInCVS(filepath: str) -> pd.DataFrame:
    if(os.path.isfile(filepath)):
        df = pd.read_csv(filepath)
        return pd.DataFrame({'streamer':df['streamer'], 'Links_To':df['Links_To'], 'count':df['count']})
    else:
        return None


def main(filepath: str):
    df = loadInCVS(filepath)
    if(df is None):
        print("File is empty")
        return

    G = nx.MultiGraph()
    with tqdm(total = df.shape[0]) as pbar:
        pbar.set_description("Loading in edges")
        for index, row in df.iterrows():
            G.add_edge(row['streamer'], row['Links_To'], weight=row['count'])
            pbar.update(1)
        
    print("Graph drawing graph")
    fig = plt.figure(figsize=(10,10))
    nx.draw_spring(G, node_size=162781)
    plt.savefig("graph.png")







if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
    except:
        print("Please provide a filepath to a csv file")
        print("Usage: python3 network.py <filepath>")
        exit()
        
    changeDefaultMPLStyle()
    main(sys.argv[1])