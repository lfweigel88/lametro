#!/usr/bin/python3
#vehicle {
#  trip {
#    trip_id: "55987526"
#    start_date: "20220520"
#    route_id: "801"
#  }
#  position {
#    latitude: 33.860725
#    longitude: -118.21622
#    bearing: 161.00594
#  }
#  current_stop_sequence: 14
#  current_status: IN_TRANSIT_TO
#  timestamp: 1653095509
#  stop_id: "80109"
#  vehicle {
#    id: "1075-1098-1130"
#    label: "1075-1098-1130"
#  }
#}
import time
import requests
import os
import json
from google.transit import gtfs_realtime_pb2
from lamvars import lamkey
import csv
feed = gtfs_realtime_pb2.FeedMessage()
feeddict = {}
stopsdict = {}
headers = {'Authorization': lamkey}
stops = requests.get("https://gitlab.com/LACMTA/gtfs_rail/-/raw/master/stops.txt")
with open('stops.csv','w') as file:
        file.write(stops.text)
with open ('stops.csv','r') as csv_file:
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
with open ('stops.json','w') as file:
        file.write(json.dumps(stopsdict))
while True:
        response = requests.get('https://api.goswift.ly/real-time/lametro-rail/gtfs-rt-vehicle-positions',headers=headers)
        feed.ParseFromString(response.content)
        i = 0
        for entity in feed.entity:
                #print(entity)
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
                        if entity.vehicle.current_status == 1:
                                feeddict[i]['status'] = "STOPPED"
                        if entity.vehicle.current_status == 2:
                                feeddict[i]['status'] = "IN TRANSIT"
                        with open('stops.csv') as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                fields = next(csv_reader)
                                for row in csv_reader:
                                        if entity.vehicle.stop_id in row:
                                                feeddict[i]['next_stop'] = str(row[2])
                                                break
                                        else:
                                                feeddict[i]['next_stop'] = "UNKNOWN"
                        #z = json.loads(x)
                        #feeddict.update(z)
                        #feeddict.
                        #print(feeddict)
                i = i + 1
        with open('lametro.json','w') as file:
                file.write(json.dumps(feeddict))
        time.sleep(30)

