#!/usr/bin/env python3.6

import requests
from asnake.aspace import ASpace
from asnake.client import ASnakeClient
import json
import csv
import os
import getpass

#This script is used to export metadata for digital objects from ASpace as CSV

#AUTHENTICATION STUFF:
aspace = ASpace()
aspace_repo = aspace.repositories(2)

#Prompt for export path to CSV
digital_object_export_csv = input('Export path for CSV: ')

digital_objects_list = aspace.client.get(aspace_repo.uri+'/digital_objects?all_ids=true').json()

with open(digital_object_export_csv,'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    #write CSV header row
    writer.writerow(["digital_object_URI", "digital_object_identifier", "digital_object_title", "digital_object_publish", "linked_instances", "file_version_uri_1","Access_Type"])

    for digital_object_id in digital_objects_list:
        do_json = aspace.client.get(aspace_repo.uri+'/digital_objects/'+str(digital_object_id)).json()
        #print (do_json)
        digital_object_URI = do_json['uri']
        digital_object_identifier = do_json['digital_object_id']
        digital_object_title = do_json['title']
        digital_object_publish = do_json['publish']

        row = [digital_object_URI, digital_object_identifier, digital_object_title, digital_object_publish]

#write data to CSV
        #Note: this only pulls the first linked instance.
        try:
            linked_instances = do_json['linked_instances'][0]['ref']
            row.append(linked_instances)
        except:
            row.append("")
            pass

        try:
            file_version_uri_1 = do_json['file_versions'][0]['file_uri']
            row.append(file_version_uri_1)
        except:
            row.append("")
            pass

        try:
            user_defined = do_json['user_defined']['enum_1']
            row.append(user_defined)
        except:
            row.append("")
            pass

        writer.writerow(row)
        print ('Exporting: ' + digital_object_URI)
