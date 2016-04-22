__author__ = 'kdenny'

import googlemaps
import json
from datetime import datetime, time, date
from pprint import pprint

from OperationalFunctions import *

# gmaps = googlemaps.Client(key='AIzaSyB17F8Q89ZuNlPN3fAXinQUDK83Bufmmto')

# gmaps = googlemaps.Client(key='AIzaSyDquQo-cF-EjYgqKLp68sXjUvmcHXTHELM')

# gmaps = googlemaps.Client(key='AIzaSyCUSkUaTU4DJhuheYoh3_x2y1BBD40N3yc')

# gmaps = googlemaps.Client(key='AIzaSyAvcHCtHqeobl8IcNlwaXbcM6LYkqkxpYo')

# gmaps = googlemaps.Client(key='AIzaSyBdvQZjLqxNDq3eDRYSWrunbrfoIONal64')

# gmaps = googlemaps.Client(key='AIzaSyB9_6Y2XDC0fAZsYBTJlEtq5wmIio65Jp8')

gmaps = googlemaps.Client(key='AIzaSyCGkffnTSjs9i0PpPXthYJ93TBSJhJHEnQ')



t = time(8, 30, 0)

d = date.today()

dt = datetime.combine(d, t)


def batchGeocodePoints(records):
    import csv
    thakeys = []
    for pointid in records:
        print pointid
        pointDict = records[pointid]
        thakeys = pointDict.keys()
        if 'lat' not in thakeys:
            thakeys.append('lat')
        if 'lon' not in thakeys:
            thakeys.append('lon')
        gresult = gmaps.geocode(pointDict['QueryAddress'])
        if len(gresult) > 0:
            geocoderesult = gmaps.geocode(pointDict['QueryAddress'])[0]['geometry']['location']
            pointDict['lat'] = geocoderesult['lat']
            pointDict['lon'] = geocoderesult['lng']


            records[pointid] = pointDict
        # alatlng = "{0},{1}".format(geocoderesult['lat'],geocoderesult['lng'])
        # latlngs.append(alatlng)

    test_file = open('C:/Users/kdenny/Documents/USPS/Data/DoSGeocode.csv','wb')
    csvwriter = csv.DictWriter(test_file, delimiter=',', fieldnames=thakeys)
    csvwriter.writerow(dict((fn,fn) for fn in thakeys))
    for uid in records:
        row = records[uid]
        csvwriter.writerow(row)
    test_file.close()


    return records

