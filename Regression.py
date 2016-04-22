__author__ = 'kdenny'

import pysal

from pysal.weights.Distance import DistanceBand
from pysal.esda import moran, getisord
# import folium
from pprint import pprint
import shapefile
import numpy as np
from OperationalFunctions import writeCSVResults

ashploc = 'C:/Users/kdenny/Documents/USPS/GIS/Revenue/DC_case_study/DC_USPS.shp'
shp = pysal.open('C:/Users/kdenny/Documents/USPS/GIS/Revenue/DC_case_study/DC_USPS.shp')
# .read with no arguments returns a list of all shapes in the file.


sf = shapefile.Reader(ashploc)
records = sf.records()
fields = sf.fields

fieldIndexDict = {}
count = 0
for f in fields:
    if count != 0:
        fieldIndexDict[f[0]] = (count - 1)
    count += 1

csaData = {}
realvalues = []


bigcount = 0
for rec in records:
    count = 0
    arecord = {}
    for item in rec:
        if count == fieldIndexDict['UFN']:
            arecord['UFN'] = item

        if count == fieldIndexDict['a15fee']:
            arecord['a15fee'] = float(item)
            realvalues.append(float(item))
            arecord['Index'] = bigcount
            bigcount += 1

        if count <= len(rec):
            count += 1

    csaData[arecord['UFN']] = arecord

pprint(realvalues)
y = np.array(realvalues)

thresh = pysal.min_threshold_dist_from_shapefile(ashploc)
dist_w = pysal.threshold_binaryW_from_shapefile(ashploc, thresh)
dist_w.transform = "B"


lg = getisord.G_Local(y,dist_w)

pprint(lg.p_sim)

psimresults = lg.p_sim.tolist()

pount = 0
frecords = []

for p in psimresults:

    for c in csaData:
        if pount == csaData[c]['Index']:
            csaData[c]['Hotspot'] = p
            frecords.append(csaData[c])
    pount += 1

pprint(frecords)
fname = 'C:/Users/kdenny/Documents/USPS/GIS/Revenue/DC_case_study/DC_USPS_results.csv'
writeCSVResults(frecords, fname)


## Join regression to points shapefile



## This is from page 283 of pysal documentation

# db = pysal.open(pysal.examples.get_path(’columbus.dbf’),’r’)

# hoval = db.by_col("HOVAL")
# y = np.array(hoval)
# y.shape = (len(hoval), 1)

# X = []
# X.append(db.by_col("INC"))
# X.append(db.by_col("CRIME"))
# X = np.array(X).T
# ols = OLS(y, X, name_y=’home value’, name_x=[’income’,’crime’], name_ds=’columbus’)
