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



if __name__ == '__main__':
    df = format(argv[1])
    df.to_csv(argv[1][:-4] + '_formated.csv', index=False)
    print(df)