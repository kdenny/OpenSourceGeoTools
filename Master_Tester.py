__author__ = 'kdenny'

from ShapefileUtils.ShpFunctions import getShpFieldData, getShpFieldIndex, addFieldToShp
from GeoJSONUtils.GeoJSONconvert import shptogeojson, is_number
from FoliumUtils.FoliumTest import makeFolium
from OperationalFunctions import writeCSVResults
from pprint import pprint
import pandas as pd
import folium

def shape_test():
    current_shp = 'C:/Users/kdenny/Documents/trade-areas/Shapefiles/DMV_Tracts_t.shp'
    new_shp = 'C:/Users/kdenny/Documents/OpenSourceTools/ShpTest.shp'

    fieldindex = getShpFieldIndex(current_shp)

    shpdata = getShpFieldData(current_shp, 'GID')

    datadict = {}
    for gid in shpdata:
        rdict = {}
        rdict['Yes'] = 1
        datadict[gid] = rdict

    addFieldToShp(current_shp, 'GID', datadict, new_shp)

    shpdata2 = getShpFieldData(new_shp, 'GID')
    pprint(shpdata2)

def geoJSONtest():
    current_shp = 'C:/Users/kdenny/Documents/OpenSourceTools/ShpTest.shp'
    new_gj = 'C:/Users/kdenny/Documents/OpenSourceTools/GJtest.geojson'
    keepFields = ['Yes']
    uidfield = 'GID'
    uidlength = 10
    shptogeojson(current_shp, new_gj, keepFields, uidfield)

def folium_test():
    # pofile = 'C:/Users/kdenny/Documents/USPS/GIS/Revenue/DC_case_study.shp'
    pofile = 'C:/Users/kdenny/Documents/USPS/GIS/CSA/CSA_Master.shp'
    gj = 'C:/Users/kdenny/Documents/USPS/GIS/USPS_Passports.geojson'
    keepFields = ['GID','PPT_Index']
    uidfield = 'GID'
    uidlength = 5


    shptogeojson(pofile, gj, keepFields, uidfield, uidlength)

    shpdata = getShpFieldData(pofile, uidfield, 5)

    gidlist = []
    afeelist = []

    for s in shpdata:
        row = shpdata[s]
        for r in row:
            if r == 'GID':
                gidlist.append(str(row[r]).zfill(5))
            if r == 'PPT_Index':
                if is_number(row[r]):
                    afeelist.append(int(row[r]))
                else:
                    afeelist.append(int(row[r]))

            if 'PPT_Index' not in row:
                afeelist.append(0)



    # csvout = 'C:/Users/kdenny/Documents/OpenSourceTools/Results.csv'
    # writeCSVResults(records,csvout)
    # point_data = pd.read_csv(csvout)
    point_data = pd.DataFrame({'GID': gidlist, 'ppt': afeelist}, index=gidlist)
    # df = pd.DataFrame({'A': [a], 'B': [b]})
    # point_data = pd.DataFrame.from_dict(mow)
    states = folium.Map(location=[48, -102], zoom_start=3)
    states.geo_json(geo_path=gj, data=point_data,
                    columns=['GID','ppt'],
                    key_on='feature.properties.GID',
                    fill_color='RdBl', fill_opacity=0.7, line_opacity=0.2,
                    legend_name='Unemployment Rate (%)')
    states.create_map(path='C:/Users/kdenny/Documents/OpenSourceTools/stamen_map2.html')



# pofile = 'C:/Users/kdenny/Documents/USPS/GIS/USPS_Passport_Final.shp'
# gj = 'C:/Users/kdenny/Documents/USPS/GIS/USPS_Passports.geojson'
#
# fi = getShpFieldIndex(pofile)
# keepfields = ['UFN','a15fee']
# uidfield = 'UFN'
#
# uidlength = 10
#
# shptogeojson(pofile,gj,keepfields,uidfield,uidlength)


# makeFolium(gj)
# geoJSONtest()

folium_test()