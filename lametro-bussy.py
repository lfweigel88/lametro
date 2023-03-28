#!/var/www/html/lametro/venv/bin/python3
#id: "4043"
#vehicle {
#  trip {
#    trip_id: "60060001631728-FEB22"
#    start_date: "20220521"
#    route_id: "60-13159"
#  }
#  position {
#    latitude: 33.98965
#    longitude: -118.22538
#    bearing: 179.90164
#    speed: 0.044704
#  }
#  current_stop_sequence: 33
#  current_status: STOPPED_AT
#  timestamp: 1653181935
#  stop_id: "12714"
#  vehicle {
#    id: "4043"
#    label: "4043"
#  }
#}
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
headers = {'Authorization': lamkey}
stops = requests.get("https://gitlab.com/LACMTA/gtfs_bus/-/raw/master/stops.txt")
with open(homedir + 'busstops.csv','w') as file:
        file.write(stops.text)
with open (homedir + 'busstops.csv','r') as csv_file:
        i = 0
        csv_reader = csv.reader(csv_file, delimiter=',')
        fields = next(csv_reader)
        for row in csv_reader:
                id = row[0]
                name = row[2]
                lat = row[4]
                long = row[5]
                stopsdict[i] = {}
                stopsdict[i]['name'] = name
                stopsdict[i]['id'] = id
                stopsdict[i]['lat'] = lat
                stopsdict[i]['long'] = long
                i = i + 1
with open (homedir + 'busstops.json','w') as file:
        file.write(json.dumps(stopsdict))
while True:
        response = requests.get('https://api.goswift.ly/real-time/lametro/gtfs-rt-vehicle-positions',headers=headers)
        feed.ParseFromString(response.content)
        i = 0
        for entity in feed.entity:
                if not entity.vehicle.trip.route_id:
                        continue
                else:
                        feeddict[i] = {}
                        #x = '{ "route_id": ' + entity.vehicle.trip.route_id + ',"latitude": ' + str(entity.vehicle.position.latitude) + ',"longitude": ' + str(entity.vehicle.position.longitude) + ',"bearing": ' + str(entity.vehicle.position.bearing) + '}'
                        feeddict[i]['route_id'] = entity.vehicle.trip.route_id
                        feeddict[i]['latitude'] = entity.vehicle.position.latitude
                        feeddict[i]['longitude'] = entity.vehicle.position.longitude
                        feeddict[i]['bearing'] = entity.vehicle.position.bearing
                        feeddict[i]['stop_id'] = entity.vehicle.stop_id
                        feeddict[i]['vehicle_id'] = entity.vehicle.vehicle.id
                        timestamp = entity.vehicle.timestamp
                        timestamp = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')
                        feeddict[i]['timestamp'] = timestamp
                        if entity.vehicle.current_status == 1:
                                feeddict[i]['status'] = "STOPPED"
                        if entity.vehicle.current_status == 2:
                                feeddict[i]['status'] = "IN TRANSIT"
                        with open(homedir + 'busstops.csv') as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                fields = next(csv_reader)
                                for row in csv_reader:
                                        if entity.vehicle.stop_id in row:
                                                feeddict[i]['next_stop'] = str(row[2])
                                                break
                                        else:
                                                feeddict[i]['next_stop'] = "UNKNOWN"
                i = i + 1
        with open(homedir + 'lametro-bus.json','w') as file:
                file.write(json.dumps(feeddict))
        time.sleep(90)
