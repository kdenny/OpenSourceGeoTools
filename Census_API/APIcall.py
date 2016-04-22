__author__ = 'kdenny'

from pprint import pprint

def getWikipedia(url):
    from bs4 import BeautifulSoup
    import urllib2

    # wiki = "http://en.wikipedia.org/wiki/List_of_postcode_districts_in_the_United_Kingdom"

    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)

    area = ""
    district = ""
    town = ""
    county = ""
    table = soup.find("table", { "class" : "wikitable sortable" })
    print table

    return table

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def queryCensusCSA(dataField, csa):
    import urllib2
    import simplejson as json
    census_key = 'fc35b71dfc10725453726fd1e8bcb1c6063db66f'

    url = 'http://api.census.gov/data/2014/acs5?get=NAME,{0}&for=combined+statistical+area:{1}&key={2}'.format(dataField, csa, census_key)
    # url = 'http://api.census.gov/data/2014/acs5?get=NAME,{0}&for=metropolitan+statistical+area/micropolitan+statistical+area:*'.format(dataField)

    conn = urllib2.urlopen(url)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def queryCensusCBSA(dataField, cbsa):
    import urllib2
    import simplejson as json
    census_key = 'fc35b71dfc10725453726fd1e8bcb1c6063db66f'

    # url = 'http://api.census.gov/data/2014/acs5?get=NAME,{0}&for=combined+statistical+area:*'.format(dataField)
    url = 'http://api.census.gov/data/2014/acs5?get=NAME,{0}&for=metropolitan+statistical+area/micropolitan+statistical+area:{1}&key={2}'.format(dataField, cbsa, census_key)

    conn = urllib2.urlopen(url)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def addFieldShp(shpfile, uidfield, datadict, newshp):
    import shapefile

    r = shapefile.Reader(shpfile)
    w = shapefile.Writer()

    fields = list(r.fields)
    w.fields = fields

    newfields = []

    fieldindex = getShpFieldIndex(shpfile)
    shpdata = getShpFieldData(shpfile, uidfield)

    for gid in shpdata:
        arecord = datadict[gid]
        drecord = shpdata[gid]
        for fn in arecord:
            if fn not in drecord and fn not in newfields:
                newfields.append(fn)


    # Add our new field using the pyshp API
    for fdn in newfields:
        if fdn not in w.fields:
            w.field(fdn, "C", "40")


    # Loop through each record, add a column.  We'll
    # insert our sample data but you could also just
    # insert a blank string or NULL DATA number
    # as a place holder

    for rec in r.records():
        uid = rec[fieldindex[uidfield]]
        if uid in datadict:
            for ft in newfields:
                if ft in datadict[uid]:
                    item = datadict[uid][ft]
                    rec.append(item)
                else:
                    rec.append(0)

        # Add the modified record to the new shapefile
        pprint(rec)
        w.records.append(rec)

    # Copy over the geometry without any changes
    w._shapes.extend(r.shapes())

    # Save as a new shapefile (or write over the old one)
    w.save(newshp)

def getShpFieldIndex(shpfile):
    import shapefile

    r = shapefile.Reader(shpfile)

    fields = list(r.fields)

    fieldIndexDict = {}
    count = 0
    for f in fields:
        if count != 0:
            fieldIndexDict[f[0]] = (count - 1)
        count += 1

    return fieldIndexDict

def getShpFieldData(shpfile, uidfield):
    import shapefile

    fieldindex = getShpFieldIndex(shpfile)
    shpdata = {}


    r = shapefile.Reader(shpfile)

    for rec in r.records():
        rdict = {}
        uid = rec[fieldindex[uidfield]]

        for f in fieldindex:
            fdata = rec[fieldindex[f]]
            if is_number(fdata) == True:
                rdict[f] = fdata
            else:
                rdict[f] = str(fdata).strip()

        shpdata[uid] = rdict

    return shpdata

def getCensusData(dataFields, dataDict):
    newData = {}
    for alias in dataFields:
        census_code = dataFields[alias]
        count = 0
        for gid in dataDict:
            print count
            if gid not in newData:
                newData[gid] = {}
            type = str(dataDict[gid]['Type'])

            if type == 'CBSA':
                r = queryCensusCBSA(census_code, gid)[1][1]
                newData[gid][alias] = float(r)
                # pprint(newData)
            elif type == 'CSA':
                r = queryCensusCSA(census_code, gid)[1][1]
                newData[gid][alias] = float(r)
                # pprint(newData)
            count += 1

    return newData

def addPop(dataField, alias, polygonmerge):
    import arcpy

    cursor = arcpy.UpdateCursor(polygonmerge)
    for row in cursor:
        gid = str(row.getValue('GID'))
        type = str(row.getValue('Type'))

        pprint(type)
        if type == 'CBSA':
            r = queryCensusCBSA(dataField, gid)[1][1]
        elif type == 'CSA':
            r = queryCensusCSA(dataField, gid)[1][1]

        pprint(r)
        row.setValue(alias, r)

        cursor.updateRow(row)


        # pprint(r)


    del row, cursor

def FieldExist(featureclass, fieldname):
    import arcpy
    fieldList = arcpy.ListFields(featureclass, fieldname)

    fieldCount = len(fieldList)

    if (fieldCount == 1):
        return True
    else:
        return False