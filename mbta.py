#!/usr/bin/python3
import time
import requests
import os
import json
from google.transit import gtfs_realtime_pb2
from lamvars import homedir
from datetime import datetime
feed = gtfs_realtime_pb2.FeedMessage()
while True:
        response = requests.get('https://cdn.mbta.com/realtime/VehiclePositions.pb')
        feed.ParseFromString(response.content)
        i = 0
        feeddict = {}
        for entity in feed.entity:
            if 'speed' in str(entity):
                print(entity)
                i = str(entity.id)
                if i in feeddict:
                    print("Duplicate!")
                    if feeddict[i]['utctimestamp'] < entity.vehicle.timestamp:
                        continue
                feeddict[i] = {}
                feeddict[i]['route_id'] = entity.vehicle.trip.route_id
                feeddict[i]['latitude'] = entity.vehicle.position.latitude
                feeddict[i]['longitude'] = entity.vehicle.position.longitude
                feeddict[i]['bearing'] = entity.vehicle.position.bearing
                feeddict[i]['stop_id'] = entity.vehicle.stop_id
                feeddict[i]['vehicle_id'] = entity.vehicle.vehicle.id
                if entity.vehicle.current_status == 2:
                    feeddict[i]['status'] = 'IN_TRANSIT_TO'
                elif entity.vehicle.current_status == 1:
                    feeddict[i]['status'] = 'STOPPED AT'
                feeddict[i]['current_status'] = entity.vehicle.current_status
                speed = (float(entity.vehicle.position.speed) * 2.23694)
                feeddict[i]['speed'] = speed
                feeddict[i]['utctimestamp'] = entity.vehicle.timestamp
                timestamp = entity.vehicle.timestamp
                timestamp = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                feeddict[i]['timestamp'] = timestamp
        with open(homedir + 'mbta.json','w') as file:
            file.write(json.dumps(feeddict))
        time.sleep(30)
