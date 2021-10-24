from dotenv import dotenv_values
from pprint import pprint as pprint
from tqdm import tqdm
import requests as request
import pandas as pd
import json 
import time
import os
import sys, getopt

import cProfile
import re
import pstats
import time



config = dotenv_values('.env')

# dictionary that holds the name and the cursor for the last list generated
visitedStreamers = {}
visitedFollowers = {}
dataframes = []
depth = 4
streamers_json = {}
streamers_json_by_id = {} 
pbar = None
SFS_count = 0
streamer_follower_count = {}

headers = {'Client-Id': config['client_id'], 'Authorization': config['app_access_token']}


def getId(json: json) -> int:
    if('data' not in json or json['data'] == []): 
        return 141981764
    id = json['data'][0]['id']
    return id

def getIdByName(streamer: str) -> int:
    if(streamer in streamers_json): return streamers_json[streamer]['id']

    params = {'login': streamer}
    try:
        req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return getIdByName(streamer)

    return getId(req.json())

def split_list_in_half(list:list):
    length = len(list)
    return list[:len(list)//2], list[len(list)//2:]

def remove_all_duplicates_in_ordered_list(list: list) -> list:
    dict = countListInstancesOrdered(list)
    list = []
    for key in dict:
        for i in range(0, dict[key]):
            list.append(key)
    return list


def fill_streamers_json(list: list):
    list = remove_all_duplicates_in_ordered_list(list)
    if(len(list) > 50):
        l1, l2 = split_list_in_half(list)
        fill_streamers_json(l1)
        fill_streamers_json(l2)
        return
        

    params = {'login': list}
    try:
        req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        fill_streamers_json(list)

    if('data' in req.json()):
        for data in req.json()['data']:
            if(data['login'] in streamers_json): continue
            streamers_json[data['login']] = data

    
def getFollowers(streamer: str) -> dict:
    id = getIdByName(streamer)
    params = {'to_id': id}
    if( streamer in visitedStreamers ): 
        propigation = visitedStreamers[streamer]['cursor']
        params.update({'after': propigation})
    try:
        req = request.get('https://api.twitch.tv/helix/users/follows?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return getFollowers(streamer)
    
    streamer_follower_count.update({streamer: req.json()['total']})
    return req.json()

def getFollows(follower_id: int) -> dict:
    params = {'from_id': follower_id}
    # name = getNameByID(follower_id)
    if( follower_id in visitedFollowers ): 
        if('cursor' in visitedFollowers[follower_id]):
            propigation = visitedFollowers[follower_id]['cursor']
            params.update({'after': propigation})
    try:
        req = request.get("https://api.twitch.tv/helix/users/follows?", headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return getFollows(follower_id)
    

    return req.json()

def getNameByID(follower_id: int):
    params = {'id' : follower_id}
    try:
        req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return getNameByID(follower_id)
    
    return req.json()['data'][0]['display_name']

def is_partnered(streamer: str):
    if(streamer in streamers_json):
        try:
            return streamers_json[streamer]['broadcaster_type']['partner']
        except:
            return False
    params = {'login': streamer}
    try:
        req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return is_partnered(streamer)
    
    try:
        return req.json()['data'][0]['broadcaster_type'] == 'partner'
    except:
        return False
        

def streamerToFollowersToStreamers(streamer: str) -> dict:

    followers = getFollowers(streamer)

    if(streamer in streamers_json):
        if('broadcaster_type' not in streamers_json[streamer] and streamers_json[streamer]['broadcaster_type'] != 'partnered'): 
            return []

    if(streamer in streamer_follower_count):
        if(streamer_follower_count[streamer] < 900000):
            return []

    if ('pagination' in followers): 
        assignCursorToStreamer(streamer, followers['pagination'])

    list = []
    if( 'data' not in followers):  
        return []
    
    for i in range(0, len(followers['data'])):
        try:
            user_follows_Json = getFollows(followers['data'][i]['from_id'])
            user_follows_data = user_follows_Json['data']
        except Exception as e:
            continue

        if('from_id' in user_follows_data):
            user = user_follows_data[0]['from_id']
            if('pagination' in user_follows_Json):
                assignCursorToFollower(user, user_follows_Json['pagination'])
        for i in range(0, len(user_follows_data)):
            alsoFollows = user_follows_data[i]['to_name']
            if(alsoFollows == streamer): 
                continue
            list.append(alsoFollows)

    list.sort()
    if(len(list) == 0): 
        return streamerToFollowersToStreamers(streamer)

    return list

def getFollowerCount(streamer: str):
    id = getIdByName(streamer)
    params = {'to_id': id}
    try:
        req = request.get('https://api.twitch.tv/helix/users/follows?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return getFollowerCount(streamer)
    
    return req.json()['total']

def assignCursorToStreamer(streamer: str, pagination):
    visitedStreamers[streamer] = pagination
    
def assignCursorToFollower(follower: int, pagination):
    visitedFollowers[follower] = pagination

def SFS(start_streamer: str, depth: int, came_from: str):
    
    if depth == 0: return
    pbar.set_description( ('{0} <- {1}').format(came_from, start_streamer))
    l1 = streamerToFollowersToStreamers(start_streamer)
    l2 = streamerToFollowersToStreamers(start_streamer)
    list = l1 + l2
    if(list == []): 
        return
    fill_streamers_json(list)
    
    bridgeWithCount = countListInstancesOrdered(list, filter = 3)
    df_local = loadLinksIntoDataFrame(bridgeWithCount, start_streamer)
    pbar.update(df_local.shape[0])
    dataframes.append(df_local)

    for streamer in bridgeWithCount.keys():
        if(bridgeWithCount[streamer] <= 3): continue
        try:
            SFS(streamer, depth - 1, came_from + ' <- ' + start_streamer)
        except:
            continue



def loadLinksIntoDataFrame(bridgeWithCount: dict, streamer):
    keys = [streamer] * len(bridgeWithCount.keys())
    other_streamers = bridgeWithCount.keys()
    count = bridgeWithCount.values()
    data = {'streamer': keys, 'Links_To': other_streamers, 'count': count}
    df = pd.DataFrame(data)
    return df

def countListInstancesOrdered(list: list, filter = 1) -> dict:
    list.sort()
    ret = {}
    checking = list[0]
    checking_count = 1
    for element in list[1:]:
        if(not element == checking):
            if(checking_count >= filter):
                ret.update({checking: checking_count})
            checking = element
            checking_count = 1
        else:
            checking_count += 1

    if(checking_count >= filter):
        ret.update({checking: checking_count})
    return ret

def loadInCVS(filepath: str) -> pd.DataFrame:
    if(os.path.isfile(filepath)):
        df = pd.read_csv(filepath)
        return pd.DataFrame({'streamer':df['streamer'], 'Links_To':df['Links_To'], 'count':df['count']})
    else:
        return None
    
def isStreamer(streamer: str) -> bool:
    params = {'login': streamer}
    try:
        req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    except Exception as e:
        time.sleep(2)
        print(e)
        return isStreamer(streamer)

    if( 'data' not in req.json() ): return False
    return True

 
def merge_dataframes_add_V(list_of_dataframes: list) -> pd.DataFrame:
    ret = list_of_dataframes[0]
    if(list_of_dataframes[0] is None): return None
    if(len(list_of_dataframes) == 1): return ret

    for df in list_of_dataframes:
        ret = merge(ret, df)
        # pprint(ret)
    return ret

def merge(df1, df2) -> pd.DataFrame:
    df3 = pd.merge(df1, df2, on=['streamer', 'Links_To'], how='outer')
    df3 = df3.fillna(0)
    df3['count'] = df3['count_x'] + df3['count_y']
    df3.drop(['count_x'] , axis=1, inplace=True)
    df3.drop(['count_y'] , axis=1, inplace=True)
    return df3  

def network_format(df: pd.DataFrame) -> pd.DataFrame:
    source = df['streamer']
    target = df['Links_To']
    weight = df['count']
    df = pd.DataFrame({'Source': source, 'Target': target, 'Weight': weight})
    return df

def main(args):  
    streamer = args[0]
    SFS(streamer, depth, ' root')
    pbar.close()
    df = merge_dataframes_add_V(dataframes)
    df = network_format(df)
    print(df)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'links', streamer + '_links.csv'), index=False)

if __name__ == '__main__':
    print('start ... \n')
    pbar = tqdm(total = 2000)
    sys.setrecursionlimit(10000)
    pbar.set_description("Getting data")
    if(len(sys.argv) > 1 and isStreamer(sys.argv[1])):

        cProfile.run('main(sys.argv[1:])', 'output.dat')
        with open('output_time.txt', 'w') as f:
            p = pstats.Stats('output.dat', stream=f)
            p.sort_stats('time').print_stats()
        with open('output_calls.txt', 'w') as f:
            p = pstats.Stats('output.dat', stream=f)
            p.sort_stats('calls').print_stats()

    else:
        print('No or invalid streamer name provided')
        print('Usage: python3 main.py <streamer_name>')
    print('\n... end')