import pandas as pd
from sys import argv

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: python3 get_unique_streamer.py <data_file>')
        exit(1)

    df = pd.read_csv(argv[1])
    df.drop_duplicates(subset=['Source'])
    targets = df.drop_duplicates(subset=['Source'])
    targets = df['Target']
    targets = pd.DataFrame({'User': targets})
    sources = df.drop_duplicates(subset=['Source'])['Source']
    sources = pd.DataFrame({'User': sources})
    uniques = sources.merge(targets, on='User', how='outer')

    previous = pd.read_csv('./streamers.csv')
    uniques = previous.merge(uniques, on='User', how='outer')
    print(uniques)
    uniques = uniques.drop_duplicates()
    uniques.sort_values(by=['User'], inplace=True)
    uniques.to_csv('streamers.csv', index=False)
    #print(uniques)