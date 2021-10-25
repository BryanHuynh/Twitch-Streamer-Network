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
            locate = df2[(df2['Source'] == row['Source']) & (df2['Target'] == row['Target'])]
            if(not locate.empty):
                df2.loc[locate.index, 'Weight'] += row['Weight']
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
            locate = df2[(df2['Source'] == row['Source']) & (df2['Target'] == row['Target'])]
            if(not locate.empty):
                df2.loc[locate.index, 'Weight'] -= row['Weight']
            else:
                df2 = df2.append(row)
            pbar_merge.update(1)
    pbar_merge.close()
    print('\n')
    return df2


def loadInCVS(filepath: str) -> pd.DataFrame:
    if(os.path.isfile(filepath)):
        df = pd.read_csv(filepath)
        return pd.DataFrame({'Source':df['Source'], 'Target':df['Target'], 'Weight':df['Weight']})
    else:
        return None

def remove_file_extension(filepath: str) -> str:
    return filepath[:filepath.rfind('.')]

def remove_root_directory(filepath: str) -> str:
    if(filepath[:2] == './'):
        return filepath[filepath.rfind('./')+2:]
    else:
        return filepath

def get_first_word(filepath: str) -> str:
    return filepath[:filepath.find('_')]

def main(argv, flag):
    df1 = loadInCVS('complete.csv')
    for csv in argv:
        df2 = loadInCVS(csv)
        if(flag):
            df1 = subtract(df1, df2)
        else:
            df1 = merge(df1, df2)
        fileNames.append(get_first_word(remove_file_extension(remove_root_directory(csv))))
    print(fileNames)
    df1.to_csv('complete.csv', index=False)
    print(df1)

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
