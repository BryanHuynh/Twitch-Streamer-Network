import pandas as pd


def main():
    edges_df = pd.read_csv("./Edges.csv")
    nodes_df = pd.read_csv("./Nodes.csv")
    # go through each id in the nodes file, find that id in the edges file, and add top game to the column next it called "source top game"
    for index, row in nodes_df.iterrows():
        id = row["Id"]
        top_game = row["Top Game"]
        name = row['Label']
        language = row["Language"]

        edges_df.loc[edges_df['Source'] == id, 'Source Top Game'] = top_game
        edges_df.loc[edges_df['Target'] == id, 'Target Top Game'] = top_game

        # make a new column in edges_df and add sources language and target languages
        edges_df.loc[edges_df['Source'] == id, 'Source Language'] = language
        edges_df.loc[edges_df['Target'] == id, 'Target Language'] = language


        edges_df.loc[edges_df['Source'] == id, 'Source'] = name
        edges_df.loc[edges_df['Target'] == id, 'Target'] = name

        
    print(edges_df)
    # write the nodes file to a csv
    edges_df.to_csv("./analysis/nodes_with_top_games.csv", index=False)





if __name__ == '__main__':  
    main()