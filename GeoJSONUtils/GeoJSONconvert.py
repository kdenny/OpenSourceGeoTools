__author__ = 'kdenny'

import shapefile
from pprint import pprint
from ShapefileUtils.ShpFunctions import getShpFieldIndex, is_number
# import geojson

def shptogeojson(shape,outfile,keepfields,uidfield,uidlength):
    reader = shapefile.Reader(shape)

    keepfields.append(uidfield)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    fieldindex = getShpFieldIndex(shape)

    buffer = []
    for sr in reader.shapeRecords():
        atr = {}
        # pprint(sr.record)
        count = 0
        for fn in fieldindex:
            if fn in keepfields:
                fdata = sr.record[fieldindex[fn]]
                if is_number(fdata):
                    if fn == uidfield:
                        atr[fn] = str(int(float(fdata))).zfill(uidlength)
                    else:
                        atr[fn] = float(fdata)
                else:
                    atr[fn] = str(fdata).strip()

        pprint(atr)
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr))

    # write the GeoJSON file
    from json import dumps
    geojson = open(outfile, "w")
    geojson.write(dumps({"type": "FeatureCollection",\
    "features": buffer}, indent=2) + "\n")
    geojson.close()

