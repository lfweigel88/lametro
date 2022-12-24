#!/bin/python3
import requests
import time
from influxdb import InfluxDBClient
client = InfluxDBClient('192.168.69.100')
client.switch_database('amtrak')
while True:
    r = requests.get("http://localhost/lametro/amtrak.json").json()
    json_payload = []
    for train in r:
        json_body = {
            "measurement": "route_stats",
            "tags": {
                "route_id": r[train]['route_id']
            },
            "fields": {
                "latitude": r[train]['latitude'],
                "longitude": r[train]['longitude'],
                "speed": r[train]['speed'],
                "bearing": r[train]['bearing']
            }
        }
        json_payload.append(json_body)
    client.write_points(json_payload)
    time.sleep(60)
