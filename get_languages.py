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

def souper(url):
    html = cfscraper.get(url, headers=headers).content
    return soup(html, "html.parser")

def getStreamerLanaguage(streamer: str) -> str:
    url = config['website'] + "{0}".format(remove_spaces(streamer))
    page_soup = souper(url)
    list_elements = page_soup.find_all('li', {'class':'list-group-item'})
    for element in list_elements:
        try: 
            text = element.find("div").find("div").text
            if text == "Language":
                return remove_spaces(element.find_all("div")[2].text)
        except:
            pass


if __name__ == '__main__':
    df = pd.read_csv('./streamers.csv')
    df['language'] = df['language'].astype(str)
    
    for index, row in df.iterrows():
        if(pd.isnull(row['language']) or row['language'] == "[]" or row['language'] == 'nan'):
            try:    
                language = getStreamerLanaguage(row['User'])
                print("{0} : {1}".format( language, row['User'] ) )
                df.at[index, 'language'] = language
                df.to_csv('streamers.csv', index=False)
            except:
                continue
        else:
            print("{0} : {1}".format( row['language'], row['User'] ) )