import json
import requests

url = "https://steamspy.com/api.php?request=all"

result = requests.request("GET", url)

result_json = json.loads(result.text)

result_list = []#list(result_json.keys())

for key in result_json.keys() :
    result_list.append([key, result_json[key]['name']])
with open('steamId.json', 'w') as outputFile :
    json.dump(result_list, outputFile)
    
outputFile.close()
 