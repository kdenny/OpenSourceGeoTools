__author__ = 'kdenny'
from pprint import pprint

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

def getShpFieldData(shpfile, uidfield, uidlength):
    import shapefile

    fieldindex = getShpFieldIndex(shpfile)
    shpdata = {}


    r = shapefile.Reader(shpfile)
    for rec in r.records():
        rdict = {}
        uid = str(int(float(rec[fieldindex[uidfield]]))).zfill(uidlength)

        for f in fieldindex:
            fdata = rec[fieldindex[f]]
            if is_number(fdata) == True:
                if f != uidfield:
                    rdict[f] = float(fdata)
                else:
                    rdict[f] = str(int(float(fdata)))
            else:
                rdict[f] = str(fdata).strip()

        shpdata[uid] = rdict

    return shpdata

def addFieldToShp(shpfile, uidfield, datadict, newshp):
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
        uid = str(int(float(rec[fieldindex[uidfield]])))
        if uid in datadict:
            for ft in newfields:
                if ft in datadict[uid]:
                    item = datadict[uid][ft]
                    rec.append(item)
                else:
                    rec.append(0)
        pprint(rec)
        # Add the modified record to the new shapefile
        w.records.append(rec)

    # Copy over the geometry without any changes
    w._shapes.extend(r.shapes())

    # Save as a new shapefile (or write over the old one)
    w.save(newshp)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False