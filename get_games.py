from bs4 import BeautifulSoup as soup
import cfscrape
import re
import pandas as pd
from pprint import pprint
from dotenv import dotenv_values
import time as time
import random

config = dotenv_values('.env')

cfscraper = cfscrape.create_scraper()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

}

def remove_spaces(string):
    return re.sub('\s+', '', string)


def get_url(streamer: str) -> str:
    str = config['website'] + "{0}".format(remove_spaces(streamer))
    print(str)
    return str

def get_url_games(streamer: str) -> str:
    str = config['website'] + "{0}/games".format(remove_spaces(streamer))
    print(str)
    return str

def souper(url):
    html = cfscraper.get(url, headers=headers).content
    return soup(html, "html.parser")

def getGames(streamer: str) -> list:
    url = get_url_games(streamer)
    page_soup = souper(url)
    gamesTable = page_soup.find('table', {'id':'games'})
    gamesRow = gamesTable.find('tbody').find_all('tr')
    games = []
    for row in gamesRow[:5]:
        game = row.find('a').text
        games.append(game)
    print(streamer, games)
    return games


def method2(streamer: str) -> list:
    url = get_url(streamer)
    page_soup = souper(url)
    channel_games = page_soup.find('div', {'id':'channel-games'})
    entities = channel_games.find_all('a', {'class':'entity'})
    games = []
    for row in entities[:5]:
        gamesRow = row.find('div', {'data-toggle':'tooltip'})
        #print(gamesRow)
        game = gamesRow['title']
        games.append(game)
    print(streamer, games)    
    return games


def main():
    print('If theres an error its like that the website is cutting access. Use VPN as a workaround')
    df = pd.read_csv('./streamers.csv')
    df['Games'] = df['Games'].astype(object)
    for index, row in df.iterrows():
        
        if(pd.isnull(row['Games'])):
            time.sleep(random.randint(1,3))
            try:
                games = method2(row['User'])
                df.at[index, 'Games'] = games
                df.to_csv('streamers.csv', index=False)
            except:
                try:
                    games = getGames(row['User'])
                    df.at[index, 'Games'] = games
                    df.to_csv('streamers.csv', index=False)
                except:
                    print('Manual evaluation of {0} required'.format(row['User']))
                continue
                
    

    

if __name__ == '__main__':
    main()