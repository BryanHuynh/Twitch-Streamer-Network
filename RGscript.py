from pandas.core.frame import DataFrame
from dotenv import dotenv_values
import requests as request
import pandas as pd
import json 

file = 'links.csv'
config = dotenv_values('.env')
headers = {'Client-Id': config['client_id'], 'Authorization': config['app_access_token']}


def printJson(req):
    parsed = json.loads(req)
    print(json.dumps(parsed, indent=4, sort_keys=True))

def getId(req):
    id = req.json()['data'][0]['id']
    return id
def getGame(req): 
    game = req.json()['data'][0]['game_name']
    return game

def getIdByName(streamer):
    params = {'login': streamer}
    req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    return getId(req)

def getGameName(broadcaster_id):
    params = {'broadcaster_id': broadcaster_id}
    req = request.get('https://api.twitch.tv/helix/channels?', headers=headers, params=params)
    return getGame(req)


def main():  
    df = pd.read_csv(file)
    streamer_list =df['streamer'].tolist()
    sgame = []
    for element in streamer_list:
        streamer = element
        broadcaster_id = getIdByName(streamer)
        streamergame  = getGameName(broadcaster_id)
        sgame.append(streamergame)
        
    df['Streamer_Game'] = pd.DataFrame(sgame)


    game_list2 =df['Links_To'].tolist() 
    fgame = [] 
    for element in game_list2: 
        follower = element
        broadcaster_id = getIdByName(follower)
        followergame  = getGameName(broadcaster_id)
        fgame.append(followergame)
    
    df['Follower_Game'] = pd.DataFrame(fgame)
    df.to_csv('modified.csv', index = False)
    
if __name__ == '__main__':
    print('start ... \n')
    main()
    print('\n... end')
