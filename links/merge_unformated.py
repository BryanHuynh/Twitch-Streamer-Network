import sys
import pandas as pd
import os
from tqdm import tqdm



def merge(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    if(df1.shape[0] > df2.shape[0]):
        df1, df2 = df2, df1

    with tqdm(total = df1.shape[0]) as pbar_merge:
        pbar_merge.set_description("Merging dataframe with existing")
        for index, row in df1.iterrows():
            locate = df2[(df2['streamer'] == row['streamer']) & (df2['Links_To'] == row['Links_To'])]
            if(not locate.empty):
                df2.loc[locate.index, 'count'] += row['count']
            else:
                df2 = df2.append(row)
            pbar_merge.update(1)
    pbar_merge.close()
    print('\n')
    return df2

def subtract(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    if(df1.shape[0] > df2.shape[0]):
        df1, df2 = df2, df1

    with tqdm(total = df1.shape[0]) as pbar_merge:
        pbar_merge.set_description("Merging dataframe with existing")
        for index, row in df1.iterrows():
            locate = df2[(df2['streamer'] == row['streamer']) & (df2['Links_To'] == row['Links_To'])]
            if(not locate.empty):
                df2.loc[locate.index, 'count'] -= row['count']
            else:
                df2 = df2.append(row)
            pbar_merge.update(1)
    pbar_merge.close()
    print('\n')
    return df2


def loadInCVS(filepath: str) -> pd.DataFrame:
    if(os.path.isfile(filepath)):
        df = pd.read_csv(filepath)
        return pd.DataFrame({'streamer':df['streamer'], 'Links_To':df['Links_To'], 'count':df['count']})
    else:
        return None

def main(argv, flag):
    df1 = loadInCVS(argv[0])
    df2 = loadInCVS(argv[1])

    if(flag):
        df3 = subtract(df1, df2)
    else:
        df3 = merge(df1, df2)

    df3.to_csv(argv[0][:-4] + "_" + argv[1][:-4] + '.csv', index=False)
    print(df3)

def isFile(filepath: str) -> bool:
    if(os.path.isfile(filepath)):
        return True
    else:
        print( str + " File does not exist")
        return False 


if __name__ == '__main__':
    if(sys.argv[1] == '-r'):
        main(sys.argv[2:], True)
    else:
        main(sys.argv[1:], False)
