#!/var/www/html/lametro/venv/bin/python3
import time
import requests
import os
import json
from datetime import datetime
from martavars import apikey
from martavars import homedir
feeddict = {}
while True:
        response = requests.get('https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey='+apikey,verify=False)
        i = 0
        #print(response.json())
        with open(homedir + 'marta2.json', 'w') as file:
             file.write(json.dumps(response.json()))
        response = response.json()['RailArrivals']
        #print(response)
        for entity in response:
            feeddict[entity['TRAIN_ID']] = {}
            #print(entity['TRAIN_ID'])
            #print(len(feeddict))
            trainid = entity['TRAIN_ID']
            feeddict[trainid]['train_id'] = entity['TRAIN_ID']
            feeddict[trainid]['latitude'] = entity['VEHICLELATITUDE']
            feeddict[trainid]['longitude'] = entity['VEHICLELONGITUDE']
            feeddict[trainid]['bearing'] = entity['DIRECTION']
            feeddict[trainid]['next_stop'] = entity['STATION']
            feeddict[trainid]['destination'] = entity['DESTINATION']
            feeddict[trainid]['timestamp'] = entity['RESPONSETIMESTAMP']
            feeddict[trainid]['line'] = entity['LINE']
            #i = i + 1
        with open(homedir + 'marta.json','w') as file:
            file.write(json.dumps(feeddict))
        time.sleep(30)
