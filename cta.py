#!/usr/bin/python3
import requests
import os
trains = ""
j=0
for i in ["blue", "red", "G", "brn", "org", "p", "pink"]:
#for i in ["blue", "red", "G"]:
    url = 'http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=a0131bbe6079484f83b60dd09742ff40&rt='+i+'&outputType=JSON'
    print(url)
    r = requests.get(url)
    data = r.json()['ctatt']['route'][0]['train']
    length = len(data)
    if i == "G":
        i = "green"
    if i == "brn":
        i = "brown"
    if i == "org":
        i = "orange"
    if i == "p":
        i = "purple"
    if i == "pink":
        i = "magenta"
    for x in range(0,length):
        print(j,x)
        trains = trains + """
            var train"""+str(j)+""" = L.circle([\"""" + data[x]['lat'] + '\", \"' + data[x]['lon'] +"""\"], 400, {
            color: \""""+i+"""\",
            fillColor: \""""+i+"""\",
	        fillOpacity: 0.8
            }).bindPopup("Test Vehicle").addTo(trains);
        """
        j = j + 1
#print(trains)
blockoftext = """
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.js"></script>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.css" />
    <style>
      html, body {
        height: 100%;
        padding: 0;
        margin: 0;
      }
      #map {
        /* configure the size of the map */
        width: 100%;
        height: 100%;
      }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js">
        $(document).ready(function(){
      setInterval(function(){
      $("mapid").load('osmtest.html')
      }, 2000);
      });
        </script>
  </head>
  <body>
    <div id="map"></div>
    <script>
      // initialize Leaflet
      // [33.98, -118.2], 10.5
      var map = L.map('map').setView({lon: -87.8165, lat: 41.8734}, 11);

      // add the OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
      }).addTo(map);
    var trains = L.layerGroup();
    function plot()
  {
    """+trains+"""
    };
    trains.addTo(map);
    plot();
      // show the scale bar on the lower left corner
      L.control.scale().addTo(map);
    </script>
  </body>
</html>
"""
#f = open('index.html','w+')
print(blockoftext)
#f.close

