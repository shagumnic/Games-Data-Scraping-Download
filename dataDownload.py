import dataDownloadProcess
import json

try :
    num_run_process = int(input('Enter how many times do you want the download process to run (int): '))
except :
    print('The number you just entered is not valid')

with open('steamId.json', 'r') as inputFile :
    steamIds = json.load(inputFile)

inputFile.close()

num_of_steamIds = len(steamIds)
if num_of_steamIds == 0 :
    isTheEndOfList = True
else :
    isTheEndOfList = False

index = 0    
while index < num_run_process and isTheEndOfList == False:
    with open('positionToStart.txt', 'r') as posFile :
        posToStart = int(posFile.readline())
    
    posFile.close()    
    posToStartAfter = dataDownloadProcess.downloadDataProcess(posToStart, steamIds, num_of_steamIds)
    
    if posToStartAfter == posToStart :
        isTheEndOfTheList = True
    
    index += 1