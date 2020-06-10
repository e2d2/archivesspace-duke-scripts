#!/usr/bin/env python3.6

import requests
from asnake.aspace import ASpace
from asnake.client import ASnakeClient
import json
import csv
import os
import getpass
import uuid

# Code borrowed from duke_create_do_from_ao_uri.py

#WARNING: USE AT YOUR OWN RISK, PROBABLY NEEDS MORE TESTING

# Starting with an input CSV, this script will use the ArchivesSpace API to batch create digital object records and link them as instances of specified archival objects.

# This script assumes you have the Archival Object URIs already. Another script exists with similar functionality if you have only refIDs and need the API to search for the URIs.

# The script will write out a CSV containing the same information as the starting CSV plus
# the refIDs and URIs for the archival objects and the the URIs for the created digital objects.

# The 7 column input csv should include a header row and be formatted with the columns identified on line 44:
# Input CSV can be modified to supply additional input metadata for forming the archival or digital objects

#AUTHENTICATION STUFF:
aspace = ASpace()
repo = aspace.repositories(2)

#FILE INPUT / OUTPUT STUFF:
#prompt for input file path
archival_object_csv = input("Path to input CSV: ")

#prompt for output path
updated_archival_object_csv = input("Path to output CSV: ")

#Open Input CSV and iterate over rows
with open(archival_object_csv,'r') as csvfile, open(updated_archival_object_csv,'wb') as csvout:
    csvin = csv.reader(csvfile)
    next(csvin, None) #ignore header row
    csvout = csv.writer(csvout)
    for row in csvin:

#INPUT CSV STUFF. This assumes you have URIs for the already created archival objects. The URI should be formatted like: #/repositories/2/archival_objects/407720

#Get info from CSV
        record_uri = row[0]

        print ('Looking up record: ' + record_uri)
        try:
            record_json = aspace.client.get(record_uri).json()

            print ('Found' + record_json['uri'])

            record_update = aspace.client.delete(record_uri).json()
            print ('Status: ' + record_update['status'])
#print confirmation that record was deleted. Response should contain any warnings
            row.append(record_update['status'])
        except:
            print ('error on record: ' + record_uri)
            row.append('ERROR- not processed')

        with open(updated_archival_object_csv,'w') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)
        #print a new line to the console, helps with readability
        print ('\n')
print ("All done")
