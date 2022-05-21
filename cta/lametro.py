#!/usr/bin/python3
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
	feeddict = feeddict + "{'"+entity.vehicle.trip.route_id+"': {'vehicle_id:' '"+entity.vehicle.vehicle.id+"' }"
print(feeddict)
