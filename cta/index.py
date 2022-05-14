#!/usr/bin/python3
import time
import requests
import os
import json
from ctavars import homedir
from ctavars import ctakey
from ctavars import metraauth
from ctavars import metrakey
while(True):
    ctajson = {}
    for i in ["blue", "red", "G", "brn", "org", "p", "pink"]:
    #for i in ["blue", "red", "G"]:
        url = 'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key='+ctakey+'&rt='+i+'&outputType=JSON'
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
    myjson2 = open(homedir + 'cta.json','w')
    myjson2.write(ctajson)
    myjson2.close()
    data = requests.get('https://gtfsapi.metrarail.com/gtfs/positions',auth=(metraauth,metrakey))
    myjson = open(homedir + 'metra.json','w')
    myjson.write(json.dumps(data.json()))
    myjson.close()
    time.sleep(15)
