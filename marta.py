#!/usr/bin/python3
import time
import requests
import os
import json
from datetime import datetime
from martavars import apikey
from martavars import homedir
feeddict = {}
while True:
        response = requests.get('https://developerservices.itsmarta.com:18096/railrealtimearrivals?apiKey='+apikey)
        i = 0
        response = response.json()['RailArrivals']
        for entity in response:
            feeddict[i] = {}
            feeddict[i]['train_id'] = entity['TRAIN_ID']
            feeddict[i]['latitude'] = entity['VEHICLELATITUDE']
            feeddict[i]['longitude'] = entity['VEHICLELONGITUDE']
            feeddict[i]['bearing'] = entity['DIRECTION']
            feeddict[i]['next_stop'] = entity['STATION']
            feeddict[i]['destination'] = entity['DESTINATION']
            feeddict[i]['timestamp'] = entity['RESPONSETIMESTAMP']
            feeddict[i]['line'] = entity['LINE']
            i = i + 1
        with open(homedir + 'marta.json','w') as file:
                file.write(json.dumps(feeddict))
        time.sleep(30)