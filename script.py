from dotenv import dotenv_values
from pprint import pprint as pprint
from tqdm import tqdm
import requests as request
import pandas as pd
import json 
import time
import os
import sys, getopt


config = dotenv_values('.env')

# dictionary that holds the name and the cursor for the last list generated
visitedStreamers = {}
visitedFollowers = {}
dataframes = []
depth = 5
pbar = None
SFS_count = 0

headers = {'Client-Id': config['client_id'], 'Authorization': config['app_access_token']}

def printJson(t: json):
    parsed = json.loads(t)
    print(json.dumps(parsed, indent=4, sort_keys=True))

def getId(json: json) -> int:
    if('data' not in json): 
        return 141981764
    id = json['data'][0]['id']
    return id

def getIdByName(streamer: str) -> int:
    params = {'login': streamer}
    req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    # print(req.json())
    return getId(req.json())

def getFollowers(streamer: str) -> dict:
    id = getIdByName(streamer)
    params = {'to_id': id, }
    if( streamer in visitedStreamers ): 
        propigation = visitedStreamers[streamer]['cursor']
        params.update({'before': propigation})

    req = request.get('https://api.twitch.tv/helix/users/follows?', headers=headers, params=params)
    return req.json()

def getFollows(follower_id: int) -> dict:
    params = {'from_id': follower_id}
    # name = getNameByID(follower_id)
    if( follower_id in visitedFollowers ): 
        propigation = visitedFollowers[follower_id]['cursor']
        params.update({'before': propigation})
    req = request.get("https://api.twitch.tv/helix/users/follows?", headers=headers, params=params)
    return req.json()

def getNameByID(follower_id: int):
    params = {'id' : follower_id}
    req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    #pprint(req.json())
    return req.json()['data'][0]['display_name']


def streamerToFollowersToStreamers(streamer: str):
    followers = getFollowers(streamer)
    if ('pagination' in followers): 
        assignCursorToStreamer(streamer, followers['pagination'])

    list = []
    if( 'data' not in followers):  
        return []

    for i in range(0, len(followers['data'])):

        try:
            followsJson = getFollows(followers['data'][i]['from_id'])
            if( 'data' not in followsJson ): 
                continue
            user = followsJson['data'][0]['from_id']
            if('pagination' in followsJson):
                assignCursorToFollower(user, followsJson['pagination'])

        except:
            continue

        for i in range(0, len(followsJson['data']) ):
            pbar.update(1)
            try:
                alsoFollows = followsJson['data'][i]['to_name']
                if streamer == alsoFollows: continue
                list.append(alsoFollows)
            except:
                continue
            
    list.sort()
    return list

def assignCursorToStreamer(streamer: str, pagination):
    visitedStreamers[streamer] = pagination
    
def assignCursorToFollower(follower: int, pagination):
    visitedFollowers[follower] = pagination


def SFS(start_streamer: str, depth: int):
    if depth == 0: return
    
    try:
        list = streamerToFollowersToStreamers(start_streamer)
        df_local = loadLinksIntoDataFrame(start_streamer, list)
        dataframes.append(df_local)
        for streamer in list:
            SFS(streamer, depth - 1)
    except:
        return


def loadLinksIntoDataFrame(streamer, list):
    bridgeWithCount = countListInstancesOrdered(list)

    keys = [streamer] * len(bridgeWithCount.keys())
    other_streamers = bridgeWithCount.keys()
    count = bridgeWithCount.values()

    data = {'streamer': keys, 'Links_To': other_streamers, 'count': count}
    df = pd.DataFrame(data)
    return df

def countListInstancesOrdered(list: list) -> dict:
    dict = {}
    checking = list[0]
    checking_count = 1
    for element in list:
        if(element is not checking):
            dict.update({checking: checking_count})
            checking = element
            checking_count = 1
        else:
            checking_count += 1
    return dict

def loadInCVS(filepath: str) -> pd.DataFrame:
    if(os.path.isfile(filepath)):
        df = pd.read_csv(filepath)
        return pd.DataFrame({'streamer':df['streamer'], 'Links_To':df['Links_To'], 'count':df['count']})
    else:
        return None
    

def merge(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
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


def main(args):  
    previous_data = loadInCVS('links.csv')

    streamer = args[0]
    SFS(streamer, depth)
    pbar.close()

    df = pd.concat(dataframes, ignore_index=True)
    if(previous_data is not None):
        df = merge(df, previous_data)
    
    print(df)
    df.to_csv('links.csv')
    print(f'\n\nTotal SFS: {SFS_count}')

    
    

if __name__ == '__main__':
    print('start ... \n')
    pbar = tqdm(total = 1000000000)
    pbar.set_description("Getting data")

    main(sys.argv[1:])
    print('\n... end')