#!/usr/bin/python3
import time
import requests
import os
import json
while(True):
    ctajson = {}
    for i in ["blue", "red", "G", "brn", "org", "p", "pink"]:
    #for i in ["blue", "red", "G"]:
        url = 'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=a0131bbe6079484f83b60dd09742ff40&rt='+i+'&outputType=JSON'
        print(url)
        r = requests.get(url)
        try:
            data = r.json()['ctatt']['route'][0]['train']
            ctajson[i] = data
        except NameError:
            continue
        except KeyError:
            continue
    ctajson = str(ctajson).replace('None','\'None\'')
    ctajson = str(ctajson).replace('O\'Hare','OHare')
    ctajson = str(ctajson).replace('\'','\"')
    myjson2 = open('/home/pi/cta/cta.json','w')
    myjson2.write(ctajson)
    myjson2.close()
    data = requests.get('https://gtfsapi.metrarail.com/gtfs/positions',auth=('b3bde87cd47fd08de2fae05d87816519','69cae6d7a74d5b246e2577fdc0c9dbd9'))
    myjson = open('/home/pi/cta/metra.json','w')
    myjson.write(json.dumps(data.json()))
    myjson.close()
    time.sleep(15)
