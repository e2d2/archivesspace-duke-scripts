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
updated_archival_object_csv = archival_object_csv + "-out.csv"

#Open Input CSV and iterate over rows
with open(archival_object_csv,'r') as csvfile, open(updated_archival_object_csv,'w', newline='') as csvout:
    csvin = csv.reader(csvfile)
    next(csvin, None) #ignore header row
    csvout = csv.writer(csvout)
    for row in csvin:

#INPUT CSV STUFF. This assumes you have URIs for the already created archival objects. The URI should be formatted like: #/repositories/2/archival_objects/407720

        ao_uri = row[0]
        new_do_url = row[5]
        #new_do_use_statement = row[2]
        new_do_id = row[3]
        new_do_title = row[1]
        Type = row[4]
        publish_true_false = row[6]

        print ('Found AO: ' + ao_uri)

        # Submit a get request for the archival object and store the JSON
        archival_object_json = aspace.client.get(ao_uri).json()
        #print(archival_object_json)

        # Add the archival object uri to the row from the csv to write it out at the end
        row.append(ao_uri)

        # If you want to reuse the display string from the archival object as the digital object title, uncomment line 86 and replace
        # 'title':new_do_title in line 89 with 'title':display_string
        # Note: this also does not copy over any notes from the archival object

		#display_string = archival_object_json['display_string']

        # Form the digital object JSON using the display string from the archival object and the identifier and the file_uri from the csv
        new_digital_object_json = {'title':new_do_title + ' [' + Type + ']','digital_object_id':new_do_id,'file_versions':[{'file_uri':new_do_url}],'user_defined':{'enum_1':Type}}
        dig_obj_data = json.dumps(new_digital_object_json)
        #print(dig_obj_data)

        # Post the digital object
        dig_obj_post = aspace.client.post('repositories/2/digital_objects',data=dig_obj_data).json()
        print(dig_obj_post)
        print('New DO: ', dig_obj_post['status'])

        # Grab the digital object uri
        dig_obj_uri = dig_obj_post['uri']
        print('New DO URI: ', dig_obj_uri)

        #publish the digital object
        if publish_true_false == 'TRUE':
            print ('Publishing DO: ' + dig_obj_uri)
            dig_obj_publish_all = aspace.client.post(dig_obj_uri + '/publish') #EEF not tested


        # Add the digital object uri to the row from the csv to write it out at the end
        row.append(dig_obj_uri)

        # Build a new instance to add to the archival object, linking to the digital object
        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}
        print (dig_obj_instance)
        # Append the new instance to the existing archival object record's instances
        archival_object_json['instances'].append(dig_obj_instance)
        archival_object_data = json.dumps(archival_object_json)
        #print (archival_object_data)
        # Repost the archival object
        archival_object_update = aspace.client.post(ao_uri,data=archival_object_data).json()

        print ('New DO added as instance of new AO: ', archival_object_update['status'])

        # Write a new csv with all the info from the initial csv + the ArchivesSpace uris for the archival and digital objects
        # overwrites every digital object, needs work

        with open(updated_archival_object_csv,"w", newline='') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)

        #print a new line for readability in console
        print ('\n')
