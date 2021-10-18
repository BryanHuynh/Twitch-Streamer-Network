from dotenv import dotenv_values
from pprint import pprint as pprint
import requests as request
import json 

config = dotenv_values('.env')

# dictionary that holds the name and the cursor for the last list generated
visitedStreamers = {}
visitedFollowers = {}
links = {}

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
    params = {'to_id': id}
    if( streamer in visitedStreamers ): 
        propigation = visitedStreamers[streamer]['cursor']
        params.update({'before': propigation})

    req = request.get('https://api.twitch.tv/helix/users/follows?', headers=headers, params=params)
    return req.json()

def getFollows(follower_id: int) -> dict:
    params = {'from_id': follower_id}
    name = getNameByID(follower_id)
    if( name in visitedStreamers ): 
        propigation = visitedStreamers[name]['cursor']
        params.update({'before': propigation})
    req = request.get("https://api.twitch.tv/helix/users/follows?", headers=headers, params=params)
    return req.json()

def getNameByID(follower_id: int):
    params = {'id' : follower_id}
    req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    #pprint(req.json())
    return req.json()['data'][0]['display_name']

def getGameByID(id: int) -> str:
    params = {'id': id}
    req = request.get("https://api.twitch.tv/helix/games", headers=headers, params=params)
    return req.json()['data'][0]['name']

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
            user = followsJson['data'][0]['from_name']
            if('pagination' in followsJson):
                assignCursorToFollower(user, followsJson['pagination'])

        except:
            continue

        for i in range(0, len(followsJson['data'])):

            try:
                alsoFollows = followsJson['data'][i]['to_name']
                
                if streamer == alsoFollows: continue
                list.append(alsoFollows)

            except:
                continue
    
    return list

def assignCursorToStreamer(streamer: str, pagination):
    visitedStreamers[streamer] = pagination
    
def assignCursorToFollower(follower: str, pagination):
    visitedFollowers[follower] = pagination


def addLinks(from_streamer: str, to_streamers: list):
    for to_streamer in to_streamers:
        addLink(from_streamer, to_streamer)
    links[from_streamer].sort()
    pprint(links[from_streamer])

def addLink(from_streamer: str, to_streamer: str):
    if(from_streamer not in links):
        links[from_streamer] = [] 
    links[from_streamer].append(to_streamer)


def SFS(start_streamer: str, depth: int):
    if depth == 0: return
    list = streamerToFollowersToStreamers(start_streamer)
    addLinks(start_streamer, list)
    for streamer in list:
        SFS(streamer, depth - 1)


def main():  
    # print(config)
    streamer = 'TenZ'
    # streamerToFollowersToStreamers(streamer)
    # pprint(visitedStreamers)
    # pprint(visitedFollowers)
    SFS(streamer, 2)
    pprint(links)




if __name__ == '__main__':
    print('start ... \n')
    main()
    print('\n... end')