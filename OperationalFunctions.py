__author__ = 'kdenny'
from pprint import pprint

def readCSV(csvfile,fieldnames):
    import csv
    records = {}
    floc = csvfile
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            rowdict = dict()
            if csvfile == 'C:/Users/kdenny/Documents/USPS/Data/Passport_Loc_UFN.csv':
                UFNid = str(row['UFN']).zfill(10)
            elif csvfile == 'C:/Users/kdenny/Documents/USPS/Data/Operating_Models/Passport_Loc_Operating_Models.csv':
                UFNid = str(row['UFN']).zfill(10)
            elif csvfile == 'C:/Users/kdenny/Documents/USPS/Data/USPS_Facilities.csv':
                UFNid = str(row['FACIL_ID']).zfill(6) + str(row['SFAS_CODE']).zfill(4)
            # pprint(fieldnames)
            for fn in fieldnames:
                if fieldnames[fn] in row:
                    rowdict[fn] = str(row[fieldnames[fn]]).strip().replace("$","").replace(",","")
                else:
                    if csvfile == 'C:/Users/kdenny/Documents/USPS/Data/Operating_Models/Passport_Loc_Operating_Models.csv':
                        print(row)

            records[UFNid] = rowdict
            # records.append(zip.zfill(5))


    return records

def readCSVtoGeocode(csvfile,fieldnames,uidfield):
    import csv
    records = {}
    floc = csvfile
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            rowdict = dict()
            uid = str(row[fieldnames[uidfield]]).zfill(6)

            for fn in fieldnames:
                rowdict[fn] = str(row[fieldnames[fn]]).strip().replace("$","").replace(",","")


            if 'P.O.' not in str(row['street']) and 'PO BOX' not in str(row['street']):
                rowdict['QueryAddress'] = '{0} {1},{2}'.format(rowdict['Street'], rowdict['City'], rowdict['State'])
            else:
                rowdict['QueryAddress'] = '{0}, {1}'.format(rowdict['City'], rowdict['State'])


            if rowdict['Postal'] == 'N':
                records[uid] = rowdict

            # records.append(zip.zfill(5))


    return records


def writeCSVResults(records,fname):
    import csv
    arecord = records[0]

    with open(fname, 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, arecord.keys())
        w.writeheader()
        for rn in records:
            w.writerow(rn)


def readCSVtoGeocodeMissing(csvfile,fieldnames,uidfield):
    import csv
    records = {}
    floc = csvfile
    nonTextFields = ['a15fee', 'p15fee', 'a14fee', 'p14fee', 'a13fee', 'p13fee', 'a12fee', 'p12fee']
    with open(floc, 'rU') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            rowdict = dict()
            uid = str(row[fieldnames[uidfield]]).zfill(6)

            for fn in fieldnames:
                rowdict[fn] = str(row[fn]).strip().replace("$","").replace(",","")
                if fn in nonTextFields:
                    if (rowdict[fn] == ' ') or (is_number(rowdict[fn]) == False):
                        rowdict[fn] = 0


            rowdict['QueryAddress'] = '{0} {1},{2}'.format(rowdict['ADDRESS'], rowdict['CITY_NAME'], rowdict['STATE'])



            records[uid] = rowdict

            # records.append(zip.zfill(5))


    return records