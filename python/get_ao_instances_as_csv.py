#!/usr/bin/env python3.6
#put a file called .archivessnake.yml in your home directory with login info. See sample file.

import time
from asnake.aspace import ASpace
from asnake.client import ASnakeClient
import requests
import json
import csv
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta, date

aspace = ASpace()

#defines repository and collection
repo = aspace.repositories(2)
ISay = input('Enter resource ID:')
collection = repo.resources(ISay)

#encoding ensures excel respects utf-8 encoding of csv file
with open(f"{collection.id_0}_archival_object_BoxFolder.csv",'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    #write CSV header row
    writer.writerow(["URI", "title", "Box", "Folder"])

    for archival_object in collection.tree.walk:
        if archival_object.level != "collection" or "series" or "subseries":

            # Handles objects without a Title, really should go pull dates out and make it the title...
            try:
                len(archival_object.title) > 0
                Title = archival_object.title
            except:
                Title = "[No title, check date field]"

            print(archival_object.uri + ' ' + Title)
            URI = title = Box = Folder = ""
            for instance in archival_object.instances:
                # Ignores digital object instances
                if instance.instance_type != "digital_object":
                    sub_container = instance.sub_container
                    top_container = sub_container.top_container.reify()

                    try:
                        len(sub_container.type_2) > 0
                        Folder = sub_container.type_2
                    except:
                        Folder = ""

                    try:
                        len(sub_container.indicator_2) >0
                        Folder_indicator = sub_container.indicator_2
                    except:
                        Folder_indicator = ""

                    print (top_container.type + " "+ top_container.indicator + " " + Folder + " " + Folder_indicator)


                writer.writerow([archival_object.uri,Title,top_container.indicator,Folder_indicator])
