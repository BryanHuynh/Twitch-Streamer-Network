from dotenv import dotenv_values
import requests as request
import json 

config = dotenv_values('.env')
headers = {'Client-Id': config['client_id'], 'Authorization': config['app_access_token']}

def printJson(req):
    parsed = json.loads(req.text)
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



def main():  
    json = getFollowers('shroud')
    print(json['data'][0])






if __name__ == '__main__':
    print('start ... \n')
    main()
    print('\n... end')