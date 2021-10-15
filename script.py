from dotenv import dotenv_values
import requests as request
import json 

config = dotenv_values('.env')
headers = {'Client-Id': config['client_id'], 'Authorization': config['app_access_token']}

def printJson(req):
    parsed = json.loads(req)
    print(json.dumps(parsed, indent=4, sort_keys=True))

def getId(req):
    id = req.json()['data'][0]['id']
    return id

def getIdByName(streamer):
    params = {'login': streamer}
    req = request.get('https://api.twitch.tv/helix/users?', headers=headers, params=params)
    return getId(req)

def getFollowers(streamer):
    id = getIdByName(streamer)
    # print(streamer, id)
    params = {'to_id': id}
    req = request.get('https://api.twitch.tv/helix/users/follows?', headers=headers, params=params)
    return req.json()

def getFollows(follower_id):
    params = {'from_id': follower_id}
    req = request.get("https://api.twitch.tv/helix/users/follows?", headers=headers, params=params)
    return req.json()

def streamerToFollowersToStreamers(streamer):
    json = getFollowers(streamer)
    list = []
    for i in range(0, len(json['data'])):
        followsJson = getFollows(json['data'][i]['from_id'])
        for i in range(0, len(followsJson['data'])):
            alsoFollows = followsJson['data'][i]['to_name']
            if streamer == alsoFollows: continue
            list.append(alsoFollows)
    return list

def main():  
    streamer = 'TenZ'
    print(streamerToFollowersToStreamers(streamer))








if __name__ == '__main__':
    print('start ... \n')
    main()
    print('\n... end')