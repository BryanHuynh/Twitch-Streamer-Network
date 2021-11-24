import pandas as pd
from sys import argv

def format(filename: str) -> pd.DataFrame:
    """
    Function to format the network data.

    Parameters
    ----------
    filename : str
        The name of the file to be read.

    Returns
    -------
    pandas.DataFrame
        The formatted data.
    """
    df = pd.read_csv(filename)
    source = df['streamer']
    target = df['Links_To']
    weight = df['count']
    ret = pd.DataFrame({'Source': source, 'Target': target, 'Weight': weight})
    return ret

def stringToArray(string):
    array = string[1:-1].split(',')
    return array

def getTopGame(string):
    if(type(string) == float or string == '[]'):
        return 'other'

    array = stringToArray(string)
    ret = array[0][1:-1]
    return ret

def node_csv():
    df = pd.read_csv('streamers.csv')
    indices = []
    names = []
    games = []
    languages = []
    for index, row in df.iterrows():
        indices.append(index)
        names.append(row['User'])
        games.append(getTopGame(row['Games']))
        languages.append(row['language'])
    ret = pd.DataFrame({'Id': indices, 'Label': names, 'Top Game': games, 'Language': languages})
    ret.to_csv('Nodes.csv', index=False)
    return ret

def edges(nodes: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_csv('links/complete.csv')
    source = []
    target = []
    weight = []
    type = []
    for index, row in df.iterrows():
        source.append(getIdByname(row['Source'], nodes))
        target.append(getIdByname(row['Target'], nodes))
        weight.append(row['Weight'])
        type.append('Directed')
    ret = pd.DataFrame({'Source': source, 'Target': target, 'Weight': weight, 'Type': type})
    print(ret)
    ret.to_csv('Edges.csv', index=False)

def getIdByname(name: str, nodes: pd.DataFrame) -> int:
    id = nodes.loc[nodes['Label'] == name]['Id'].values[0]
    #print(id)
    return id




if __name__ == '__main__':
    nodes = node_csv()
    edges = edges(nodes)
