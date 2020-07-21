import json
import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dateutil.parser import parse
import re
import time
from datetime import datetime

def getContent(url) :
    
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    #session.get(url)
    
    response = session.get(url) 
    #response = requests.request('GET', url)
    
    return BeautifulSoup(response.content, 'html.parser')
    
def steamPricesScraper(steamId) :
    #timeout = 10
    
    #attempts = 3
    
    #for attempt in range(attempts) :
    url = 'https://www.steamprices.com/us/app/' + steamId
    
    content = getContent(url)
    
    gamePrices = content.findAll('span', attrs = {'class':'price value'})
    
    #gameScore = content.findAll('div', attrs = {'class': 'metacritic_score'})
    
    gameReviewScore = content.find('div', attrs = {'class': 'review_scores'})
    
    gameRelease = content.find('span', attrs = {'class': 'release'})
    
    if gamePrices != [] : #and gameReviewScore != None and gameRelease != None : #and gameScore != [] :
        gameOriginalPrice = gamePrices[0].text
        #gameUserScore = gameScore[1].text
        posStartPrice = 2
        try :
            gameOriginalPrice = float(gameOriginalPrice[posStartPrice:])
        except :
            gameOriginalPrice = None #Free game, steam API genre is not right some times
    else :
        gameOriginalPrice = None
        #lengthIfNoScore = 7
        #if len(gameUserScore) < lengthIfNoScore :
            #gameUserScore = None
        #else :
            #gameUserScore = float(gameUserScore[lengthIfNoScore - 1:])
    if gameReviewScore is not None :
        gameReviewPercentList = re.findall("\d+%", gameReviewScore.text)
        if gameReviewPercentList != [] :
            gameReviewPercent = gameReviewPercentList[0]
            gameReviewPercent = int(gameReviewPercent[:len(gameReviewPercent)-1]) #remove the percentage symbol
        else :
            gameReviewPercent = 0
    else :
        gameReviewPercent = None
        
    if gameRelease is not None :
        posStartDate = 9
        gameReleaseDate = parse(gameRelease.text[posStartDate:])
        gameReleaseDate = gameReleaseDate.strftime('%m-%d-%Y')
    else :
        gameReleaseDate = None
    
    return gameOriginalPrice, gameReleaseDate, gameReviewPercent #gameUserScore,

def steamTagsScraper(steamId) :
    url = "https://store.steampowered.com/app/" + steamId + "/?cc=us"
    
    content = getContent(url)
    
    gameTags = content.findAll("a", attrs = {'class' : "app_tag" })
    
    gameLanguages = content.findAll("td", attrs = {'class' : "ellipsis"})
    
    gameDescription = content.find('div', attrs = {'id' : 'game_area_description'})
    
    if gameTags != [] :
        maximumTags = 5
        lenGameTags = len(gameTags)
        if lenGameTags < maximumTags :
            maximumTags = lenGameTags
        
        index_tag = 0
        gameTagsList = []
        while index_tag < maximumTags :
            posTagStart = 13
            posTagEnd = -12
            gameTag = gameTags[index_tag].text[posTagStart:]
            gameTag = gameTags[index_tag].text[-len(gameTag) + 1:posTagEnd]
            gameTagsList.append(gameTag)
            index_tag += 1
    else :
        gameTagsList = None
    
    if gameLanguages != []:
        
        gameLanguagesList = []
        numOfLanguages = len(gameLanguages)
        index_language = 0
        while index_language < numOfLanguages :
            posLangStart = 5
            posLangEnd = -3
            gameLanguage = gameLanguages[index_language].text[posLangStart:]
            gameLanguage = gameLanguages[index_language].text[-len(gameLanguage) + 1: posLangEnd]
            gameLanguagesList.append(gameLanguage)
            index_language += 1
    else :
        gameLanguagesList = None
        
    if gameDescription is not None :
        gameDescriptionLen = len(gameDescription.text)
        gameDescriptionText = gameDescription.text
    else :
        gameDescriptionLen = 0
        gameDescriptionText = None
        
    return gameTagsList, gameLanguagesList, gameDescriptionLen, gameDescriptionText

def steamChartScrapper(steamId, release_date) :
    url = 'https://steamcharts.com/app/' + steamId

    content = getContent(url)

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

def downloadDataProcess(posToStart, steamIds, num_of_steamIds) :
    
    posToEnd = posToStart + 100
    
    if posToEnd >= num_of_steamIds :
        posToEnd = num_of_steamIds
        
    #listOfGames = {}
    
    listOfGames = []
    #outputFile = open("dataForSortingAlgoVisual.json", "w")
    timeWait = 5
    
    for index in range(posToStart, posToEnd) :
        steamId = steamIds[index][0]
        name = steamIds[index][1]
        steamUrl = "http://store.steampowered.com/api/appdetails?cc=us&appids=" + steamId
        #response = requests.request('GET', steamUrl)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        #session.get(url)
        
        response = session.get(steamUrl) 
        #response = requests.request('GET', url)
        
        steamRequest = json.loads(response.text)
        if steamRequest[steamId]["success"] == True and 'genres' in steamRequest[steamId]["data"].keys() and "developers" in steamRequest[steamId]["data"].keys():
            print(steamId)
            listOfGenres = []
            for genre in steamRequest[steamId]["data"]["genres"] :
                if genre["description"] in ("RPG", "Action", "Adventure", "Casual",\
                                            "Indie", "Massively Multiplayer", "Racing",\
                                            "Simulation", "Sports", "Strategy") :
                    listOfGenres.append(genre["description"])
            if len(listOfGenres) == len(steamRequest[steamId]["data"]["genres"]) :
                gameOriginalPrice, gameReleaseDate, gameReviewPercent = steamPricesScraper(steamId)
                gameTags, gameLanguages, gameDescriptionLen, gameDescriptionText = steamTagsScraper(steamId)
                if gameOriginalPrice is not None and gameReleaseDate is not None and gameReviewPercent is not None and gameTags is not None and gameLanguages is not None :
                    release_date = datetime.strptime(gameReleaseDate, '%m-%d-%Y').date()
                    if release_date.year >= 2012 :
                        num_players_after_month = steamChartScrapper(steamId, release_date)
                        if num_players_after_month is not None :
                            
                            developers = steamRequest[steamId]["data"]["developers"]
                            
                            if "movies" in steamRequest[steamId]["data"].keys() :
                                num_of_movies = len(steamRequest[steamId]["data"]["movies"])
                            else :
                                num_of_movies = 0
                            if "screenshots" in steamRequest[steamId]["data"].keys() :
                                num_of_screenshots = len(steamRequest[steamId]["data"]["screenshots"])
                            else :
                                num_of_screenshots = 0
                            
                            #listOfGames[steamId] = {"name" : result_json[steamId]['name'],  "original_price" : gameOriginalPrice, "genres" : listOfGenres,\
                                                #"release_date" : gameRelease, "positive_review" : gameReviewPercent, "developers": developers,\
                                                #"num_of_movies" : number_of_movies, "num_of_screenshots" : number_of_screenshots,\
                                                #"game_description_len": gameDescriptionLength, "tags" : gameTags, "languages" : gameLanguages}
                            listOfGames.append([steamId, name, gameOriginalPrice, listOfGenres, gameReleaseDate, gameReviewPercent,
                                                developers, num_of_movies, num_of_screenshots, gameDescriptionLen, gameTags, gameLanguages,
                                                num_players_after_month, gameDescriptionText]) 
                            #json.dump(listOfGame, outputFile)
        time.sleep(timeWait)
    
    
    if posToStart == 0 :
        with open('dataForMachineLearning.csv', 'w', encoding='utf-8', newline='') as outputFile :
            writer = csv.writer(outputFile)
            writer.writerow(['steamId', 'name', 'original_price', 'genres', 'release_date', 'positive_review', 'developers', 'num_of_movies', 'num_of_screenshots', 'game_description_len', 'tags', 'languages', 'num_players_after_month', 'game_description'])
            writer.writerows(listOfGames)
        
    else :
        with open("dataForMachineLearning.csv", "a", encoding="utf-8", newline='') as outputFile :
            writer = csv.writer(outputFile)
            writer.writerows(listOfGames)
    
    outputFile.close()
    
    with open('positionToStart.txt', 'w', encoding="utf-8") as posFile :
        posFile.write(str(posToEnd))
    
    posFile.close()
    
    return posToEnd