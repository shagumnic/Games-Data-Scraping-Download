# Games-Data-Scraping-Download
Utilze Web Scraper and REST API to download video game's revelant data for other personal projects (videoGameRecommendation and videoGameSuccessPrediction):
- steamIdGet.py: request data from Steam's Spy's API to get a list of all the games' ID and their respective name, store that list to a json file (steamId.json).
- dataDownloadProcess.py: using the list of game's ID in the steamId.json as filter to get their respective relevant data through Web Scraping or REST API request: launch's price, critics' score, release date, genres, tags, number of game's trailers, number of game's screenshot, game's description, supported languages, number of players after a month. During the process, if any game's missing one of those data, remove them, else append them to a list of dictionary along with all of those informations. Afterwards, write the list to a csv file (dataForMachineLearning.csv) to be used for future projects.
- dataDownload.py: manage how many games per run user want to download using dataDownloadProcess. After each run, write down the current position that the program stop at to the positionToStart.txt file to resume the process afterwards.
- dataUpdateProcess.py: initially use to add a column contain game's description to the current downloaded list of game's data or remove the row that has a null column in the csv file. Doesn't need to use it anymore because that was handle later in the dataDownloadProcess.py.
- dataUpdate.py: manage which option in the dataUpdateProcess.py the user want to choose (remove row that has null column or add the description column). Doesn't need to be used anymore. 

# Tool use:
- Python
- BeautifulSoup library to scrape the necessary information from needed website.
- requests library to request content from a url for either Web Scraping or REST API usage.
- json and csv library to write the content downloaded to files for future use.
- requests retry feature to apply delays between each request of the same URL to avoid limit exceeded with those URL.
- datetime library to work with game's release date (convert them to string to write to json file and convert string to datetime to make appropriate comparision).
- re libray: use regex to find relevant content in certain string that was return by Beautiful Soup Web Scraping contents.
