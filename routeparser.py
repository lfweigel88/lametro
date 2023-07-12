#!/usr/bin/python3
import csv
with open('amtrak.csv',newline='') as csvfile:
    fieldnames = ['Name', 'Numbers']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    for row in reader:
        routename = row['Name']
        routenumber = row['Numbers']
        routenumber = routenumber.split(', ')
        for routeindex in routenumber:
            if '–' in routeindex:
                routeindex = routeindex.split('–')
                newrouteindex = range(int(routeindex[0]), int(routeindex[1]))
                print(list(newrouteindex))