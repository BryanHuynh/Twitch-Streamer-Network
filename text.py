import pandas as pd

df1 = pd.DataFrame({'A': ['A0', 'A0', 'A0', 'A0', 'A0'], 'T': ['A0', 'A1', 'A2', 'A3', 'B'], 'V':[1,1,1,1,7]})
df2 = pd.DataFrame({'A': ['A0', 'A0', 'A2', 'A3', 'C'], 'T': ['A0', 'A1', 'A2', 'A3', 'C'], 'V':[1,1,1,1,5]})
df3 = pd.DataFrame({'A': ['B0', 'B0', 'B0', 'B0', 'B0'], 'T': ['A0', 'A1', 'A2', 'A3', 'C'], 'V':[1,1,1,1,5]})
df4 = pd.DataFrame({'A': ['B0', 'B0', 'B0', 'B0', 'B0'], 'T': ['A0', 'A1', 'A2', 'A3', 'C'], 'V':[1,1,1,1,5]})
df5 = pd.DataFrame({'A': ['A1'], 'T': ['A0'], 'V':[1]})
df6 = pd.DataFrame({'A': ['A0'], 'T': ['A1'], 'V':[1]})


def merge(df1, df2):
    df3 = pd.merge(df1, df2, on=['A', 'T'], how='outer')
    df3 = df3.fillna(0)
    df3 = df3.astype(int)
    df3 = df3.sum(axis=1)
    return df3

def merge_dataframes_add_V(list_of_dataframes: list) -> pd.DataFrame:
    ret = list_of_dataframes[0]
    for df in list_of_dataframes:
        ret = merge(ret, df)
    return ret

def merge(df1, df2) -> pd.DataFrame:
    df3 = pd.merge(df1, df2, on=['A', 'T'], how='outer')
    df3 = df3.fillna(0)
    df3['V'] = df3['V_x'] + df3['V_y']
    df3.drop(['V_x'] , axis=1, inplace=True)
    df3.drop(['V_y'] , axis=1, inplace=True)
    return df3  

df = merge_dataframes_add_V([df6, df5])
print(pd.crosstab(df6['A'], df6['T']))
print(df)