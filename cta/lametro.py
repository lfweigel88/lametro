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
import urllib
from ctavars import lamkey
feed = gtfs_realtime_pb2.FeedMessage()
feeddict = ""
headers = {'Authorization': lamkey}
response = requests.get('https://api.goswift.ly/real-time/lametro-rail/gtfs-rt-vehicle-positions',headers=headers)
feed.ParseFromString(response.content)
for entity in feed.entity:
	feeddict = feeddict + "{'"+entity.vehicle.trip.route_id+"': {'vehicle_id:' '"+entity.vehicle.vehicle.id+"', 'latitude': '" + entity.vehicle.position.latitude +"', 'longitude': '" + entity.vehicle.position.longitude +"',} }"
print(feeddict)
