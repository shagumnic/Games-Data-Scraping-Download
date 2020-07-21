import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def steamChartScrapper(steamId, release_date) :
    url = 'https://steamcharts.com/app/' + steamId

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url)

    content = BeautifulSoup(response.content, 'html.parser')

    gamePlayers = content.findAll('tr')

    if gamePlayers != [] :
        date_str = gamePlayers[-2].find('td', {'class': 'month-cell left'})
        if date_str is not None :
            date_str = date_str.text
            posToStart = 6
            posToEnd = -5
            date_str = date_str[posToStart:]
            date_str = date_str[:posToEnd]
            date_datetime = datetime.strptime(date_str, '%B %Y').date()
            if date_datetime > release_date :
                num_player_after_month = gamePlayers[-2].find('td', {'class': 'right num-f'})
                if num_player_after_month is not None:
                    num_player_after_month = num_player_after_month.text
                else:
                    num_player_after_month = None
            else :
                num_player_after_month = None
        else :
            num_player_after_month = None
    else:
        num_player_after_month = None

    return num_player_after_month

def getDescription(steamId) :
    url = "https://store.steampowered.com/app/" + steamId + "/?cc=us"
    
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url)
    
    content = BeautifulSoup(response.content, 'html.parser')
    
    gameDescription = content.find('div', attrs = {'id' : 'game_area_description'})
    
    if gameDescription is not None : 
        return gameDescription.text
    else :
        return None
    #steamRequest = json.loads(response.text)
    
    #if steamRequest[steamId]["success"] == True and 'detailed_description' in steamRequest[steamId]["data"].keys() :
        #cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        #description = re.sub(cleanr, ' ', steamRequest[steamId]['data']['detailed_description'])
        ##description = BeautifulSoup(steamRequest[steamId]['data']['detailed_description'], 'html.parser').text
        #return description
    #else :
        #return None
    
def dataUpdatePlayers() :
    #df = pd.read_csv('dataForMachineLearning.csv')
    
    #for i in range(len(df.index)) :
        #release_date = datetime.strptime(df['release_date'][i], '%m-%d-%Y').date()
        #if release_date.year < 2012 :
            #df.at[i, "num_players_after_month"] = None
        #else :
            #df.at[i, "num_players_after_month"] = steamChartScrapper(str(df['steamId'][i]), release_date)
    
    #df.to_csv('dataForMachineLearning.csv', index=False)
    df = pd.read_csv('dataForMachineLearning.csv')
    
    df['description'] = ''
    for i in range(len(df.index)) :
        steamId = df['steamId'][i]
        description = getDescription(str(steamId))
        df.loc[i, 'description'] = description
        
    df = df[df.description.notnull()]
    df.to_csv('dataForRecommendation.csv', index=False)
    
def dataUpdateRemoveRowsPlayers() :
    df = pd.read_csv('dataForMachineLearning.csv')
    
    df = df[df.num_players_after_month.notnull()]
    
    df.to_csv('dataForMachineLearning.csv', index=False)
    
dataUpdatePlayers()