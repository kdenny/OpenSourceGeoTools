__author__ = 'kdenny'

from APIcall import getWikipedia, queryCensusCSA, queryCensusCBSA, addPopField, addPop, addFieldShp, getShpFieldIndex, getShpFieldData
from APIcall import getCensusData
from pprint import pprint

polygonMerge = "C:/Users/kdenny/Documents/USPS/Data/CSA/CSA_CBSA_Join_F.shp"

dataFields = {
    # 'Pop2014' : 'B01001_001E',
    'PBachDeg' : 'B15003_022E'
}

newShp = "C:/Users/kdenny/Documents/USPS/GIS/Revenue/CSA_w_Census_Data.shp"

uid = 'GID'

# addPopField(polygonMerge, alias)

# addFieldShp(polygonMerge, uid, data, )
# addPop(pop, alias, polygonMerge)

shpdata = getShpFieldData(polygonMerge, uid)

censusdata = getCensusData(dataFields, shpdata)

addFieldShp(polygonMerge, uid, censusdata, newShp)




# airportUrl = wiki = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States#Primary_airports"
# t = getWikipedia(airportUrl)
# pprint(t)
# df = 'B11001_002E'


# gid = '*'

# a = queryCensusCSA(df)
# a = queryCensusCBSA(pop, gid)
# pprint(a)



