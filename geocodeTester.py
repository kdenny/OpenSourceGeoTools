__author__ = 'kdenny'

from geocoder import *
from OperationalFunctions import readCSVtoGeocode, readCSVtoGeocodeMissing
from ArcPyFunctions import makePointShape
from pprint import pprint


## Non-Postal


csvfile = 'C:/Users/kdenny/Documents/USPS/Data/DoS/Passport_Locations_DoS_Subset_4.csv'

uidfield = 'DOS_ID'

newFields = {
    'FacName' : 'Facility Name',
    'Street' : 'street',
    'City' : 'city',
    'State' : 'state',
    'Zip' : 'Zip',
    'DOS_ID' : 'dos_fac_id',
    'Postal' : 'Postal'
}



records = readCSVtoGeocode(csvfile, newFields, uidfield)

records = batchGeocodePoints(records)

passportShpLoc = 'C:/Users/kdenny/Documents/USPS/GIS/'
passportShp = 'NonPostal_PassportLocs_F.shp'

makePointShape(records, passportShpLoc, passportShp, newFields)




## Postal

# newFieldsPassport = {'TERMTYPE' : 'TERMINAL_TYPE',
#              'PAL_or_PAC' : 'PPT_Appt_Line_PAL_or_PPT_Accept_Ctr_PAC', # Formerly, 'PPT_Appt_Line_PAL_or_PPT_Accept_Ctr_PAC'
#              'PREMIERE' : 'PREMIERE_SITE', # Formerly, 'PREMIERE_SITE'. Sites used as "Model Facilities"
#              'UFN' : 'UFN', # 10-digit UID, Unit Finance number. Built from 6-digit STATION_FINANCE_NO + 4-digit SFAS_CODE
#              'AREA_NAME' : 'AREA_NAME',
#              'DISTNAME' : 'DISTRICT_NAME', # Formerly, DISTRICT_NAME
#              'FACINAME' : 'FACILITY_NAME', # Formerly, FACILITY_NAME
#              'FIN_NUM' : 'STATION_FINANCE_NO',
#              'ADDRESS' : 'ADDRESS',
#              'CITY_NAME' : 'CITY_NAME',
#              'STATE' : 'STATE',
#              'ZIPCODE' : 'ZIPCODE',
#              'DOS_ID' : 'DOS_ID',
#              'APPT_REQ' : 'APPT_REQUIRED', # Formerly, "APPT_REQUIRED"
#              'PHOTO' : 'PHOTO_PROVIDED', # Formerly, "PHOTO_PROVIDED"
#              'PPT_AGENCY' : 'PASSPORT_AGENCY', #Formerly, "PASSPORT_AGENCY"
#              'AppFee15' : 'FY2015_PASSPORT_APPLICATION_FEES_AIC264', # Formerly, FY2015_PASSPORT_APPLICATION_FEES_AIC264
#              # 'APPNUM15' : 'FY2015_PASSPORT_APPLICATIONS_ACCEPTED', #Formerly, FY2015_PASSPORT_APPLICATIONS_ACCEPTED
#              'PhotoFee15' : 'FY2015_PHOTO_FEES_AIC241', # Formerly, FY2015_PHOTO_FEES_AIC241
#              # 'PHOTONUM15' : 'ZYXW', # Formerly, FY2014_PASSPORT_APPLICATION_FEES_AIC264
#              'AppFee14' : 'FY2014_PASSPORT_APPLICATION_FEES_AIC264', # Formerly, FY2014_PASSPORT_APPLICATION_FEES_AIC264
#              'PhotoFee14' : 'FY2014_PHOTO_FEES_AIC241',
#              'AppFee13' : 'FY2013_PASSPORT_APPLICATION_FEES_AIC264',
#              'PhotoFee13' : 'FY2013_PHOTO_FEES_AIC241', # Formerly, FY2014_PHOTO_FEES_AIC241
#              'AppFee12' : 'FY2012_PASSPORT_APPLICATION_FEES_AIC264', # Formerly, FY2014_PHOTO_FEES_AIC241
#              'PhotoFee12' : 'FY2012_PHOTO_FEES_AIC241' # Formerly, FY2014_PHOTO_FEES_AIC241
#             }
#
# uidfield = 'DOS_ID'
#
# csvfile = 'C:/Users/kdenny/Documents/USPS/Joining_Shapefiles/MissingRecords.csv'
#
# records = readCSVtoGeocodeMissing(csvfile, newFieldsPassport, uidfield)
#
# records = batchGeocodePoints(records)
#
# passportShpLoc = 'C:/Users/kdenny/Documents/USPS/GIS/'
# passportShp = 'MissingUSPSPassportLocations.shp'
#
# makePointShape(records, passportShpLoc, passportShp, newFieldsPassport)