from pprint import pprint as pprint
from dotenv import dotenv_values
import requests as request
import os

config = dotenv_values(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def getToken():
    params = {'client_id': config['client_id'], 'client_secret': config['client_secret'], 'grant_type': 'client_credentials'}
    req = request.post('https://id.twitch.tv/oauth2/token', params=params)
    pprint(req.json())

if __name__ == '__main__':
    getToken()