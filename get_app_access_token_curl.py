from pprint import pprint as pprint
from dotenv import dotenv_values
import pycurl
import os
import json
from io import BytesIO

config = dotenv_values(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def getToken():
    data = BytesIO()
    #req = request.post('https://id.twitch.tv/oauth2/token', params=params)
    #pprint(req.json())
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://id.twitch.tv/oauth2/token')
    c.setopt(c.POSTFIELDS, 'client_id=' + config['client_id'] + '&client_secret=' + config['client_secret'] + '&grant_type=client_credentials')
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    return json.loads(data.getvalue())['access_token']


if __name__ == '__main__':
    pprint(getToken())
