#!/var/www/html/lametro/venv/bin/python3
import time
import requests
import os
import json
from google.transit import gtfs_realtime_pb2
from lamvars import homedir
from datetime import datetime
import re
feed = gtfs_realtime_pb2.FeedMessage()
#headers = {'Authorization': 'ee6a9e3a4daf83773216c0f89712e69b'}
routes = ('A', 'B', 'D', 'E', 'G', 'H', 'L', 'N', 'R', 'W')
while True:
    response = requests.get("https://www.rtd-denver.com/files/gtfs-rt/VehiclePosition.pb")
    feed.ParseFromString(response.content)
    i = 0
    feeddict = {}
    for entity in feed.entity:
        #if entity.vehicle.trip.route_id == 'A' or entity.vehicle.trip.route_id == 'A':
        #if 'position' in str(entity):
        #if re.search('[a-zA-Z]', str(entity.vehicle.trip.route_id)):
        for route in routes:
            #print(entity.vehicle.trip.route_id)
            #if route in (str(entity.vehicle.trip.route_id)) and len(entity.vehicle.vehicle.label) > 4:
            if route in (str(entity.vehicle.trip.route_id)):
                #print(entity.vehicle.trip.route_id)
                #print(len(entity.vehicle.vehicle.label))
                i = str(entity.id)
                feeddict[i] = {}
                feeddict[i]['route_id'] = entity.vehicle.trip.route_id
                feeddict[i]['route_name'] = entity.vehicle.vehicle.label
                feeddict[i]['latitude'] = entity.vehicle.position.latitude
                feeddict[i]['longitude'] = entity.vehicle.position.longitude
                feeddict[i]['bearing'] = entity.vehicle.position.bearing
                feeddict[i]['vehicle_id'] = entity.vehicle.vehicle.id
                feeddict[i]['utctimestamp'] = entity.vehicle.timestamp
                feeddict[i]['current_status'] = entity.vehicle.current_status
                feeddict[i]['stop_id'] = entity.vehicle.stop_id
                timestamp = entity.vehicle.timestamp
                timestamp = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                feeddict[i]['timestamp'] = timestamp
                feeddict[i]['current_status'] = entity.vehicle.current_status
        with open(homedir + 'denver.json','w') as file:
            file.write(json.dumps(feeddict))
    time.sleep(30)
