from dotenv import dotenv_values
from pprint import pprint as pprint
import requests as request
import pandas as pd
import json 

config = dotenv_values('.env')

# dictionary that holds the name and the cursor for the last list generated
visitedStreamers = {}
visitedFollowers = {}
dataframes = []

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

    for i in range(0, min(len(followers['data']), 10000000)):

        try:
            followsJson = getFollows(followers['data'][i]['from_id'])
            if( 'data' not in followsJson ): 
                continue
            user = followsJson['data'][0]['from_id']
            if('pagination' in followsJson):
                assignCursorToFollower(user, followsJson['pagination'])

        except:
            continue

        for i in range(0, min( len(followsJson['data']), 10000000) ):

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


def main():  
    streamer = 'TenZ'
    SFS(streamer, 10)
    
    df = pd.concat(dataframes, ignore_index=True)
    print(df)
    df.to_csv('links3.csv')

if __name__ == '__main__':
    print('start ... \n')
    main()
    print('\n... end')