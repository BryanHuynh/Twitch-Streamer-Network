import pandas as pd
from sys import argv

if __name__ == '__main__':
    df = pd.read_csv(argv[1])
    df.drop_duplicates(subset=['Source'])
    targets = df.drop_duplicates(subset=['Source'])
    targets = df['Target']
    targets = pd.DataFrame({'User': targets})
    sources = df.drop_duplicates(subset=['Source'])['Source']
    sources = pd.DataFrame({'User': sources})
    #previous = pd.read_csv('./streamers.csv')
    unqiues = sources.merge(targets, on='User', how='outer')
    #unqiues = unqiues.merge(previous, on='User', how='outer')
    unqiues['Games'] = ""
    unqiues['Games'] = unqiues['Games'].astype(object)
    unqiues = unqiues.dropna()
    unqiues = unqiues.drop_duplicates()
    unqiues.sort_values(by=['User'], inplace=True)
    unqiues.to_csv('streamers.csv', index=False)
    print(unqiues)