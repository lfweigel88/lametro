#!/var/www/html/lametro/venv/bin/python3
import time
import requests
import os
import json
from google.transit import gtfs_realtime_pb2
from lamvars import lamkey
from lamvars import homedir
import csv
from datetime import datetime
feed = gtfs_realtime_pb2.FeedMessage()
feeddict = {}
stopsdict = {}
while True:
        response = requests.get('https://asm-backend.transitdocs.com/gtfs/amtrak')
        feed.ParseFromString(response.content)
        i = 0
        for entity in feed.entity:
            if 'IN_TRANSIT_TO' in str(entity) or 'STOPPED' in str(entity):
                print(entity)
                feeddict[i] = {}
                #x = '{ "route_id": ' + entity.vehicle.trip.route_id + ',"latitude": ' + str(entity.vehicle.position.latitude) + ',"longitude": ' + str(entity.vehicle.position.longitude) + ',"bearing": ' + str(entity.vehicle.position.bearing) + '}'
                feeddict[i]['route_id'] = entity.vehicle.trip.route_id
                feeddict[i]['latitude'] = entity.vehicle.position.latitude
                feeddict[i]['longitude'] = entity.vehicle.position.longitude
                feeddict[i]['bearing'] = entity.vehicle.position.bearing
                feeddict[i]['stop_id'] = entity.vehicle.stop_id
                feeddict[i]['vehicle_id'] = entity.vehicle.vehicle.id
                feeddict[i]['speed'] = entity.vehicle.position.speed
                if entity.vehicle.current_status == 2:
                    feeddict[i]['status'] = 'IN_TRANSIT_TO'
                elif entity.vehicle.current_status == 1:
                    feeddict[i]['status'] = 'STOPPED AT'
                timestamp = entity.vehicle.timestamp
                timestamp = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                feeddict[i]['timestamp'] = timestamp
            i = i + 1
        with open(homedir + 'amtrak.json','w') as file:
                file.write(json.dumps(feeddict))
        time.sleep(30)

