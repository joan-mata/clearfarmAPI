from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db

def downloadData(data):
    csvFilePath = 'app/downloads/csv/dataDownload.csv'
    jsonFilePath = 'app/downloads/dataDownload.json'

#    with open(csvFilePath, 'w', encoding='utf-8') as csvfile:
#        csvfile.write(json.dumps(data, indent=4))

    dataJsonObj = json.loads(json_util.dumps(data))

    #upload JSON file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsfile:
        json.dump(dataJsonObj, jsfile, indent=4)
    
    #upload CSV files
    iteration = 1
    csvAuxPath = csvFilePath[:-4]
    for item in dataJsonObj:
        csvEndPath = csvAuxPath + str(iteration) + '.csv'
        iteration += 1
        
        df = pd.json_normalize(item)
        df.to_csv(csvEndPath)


#        with open(csvEndPath, 'w') as f:
#            wr = csv.DictWriter(f, fieldnames = item[0].keys())
#            wr.writeheader()
#            wr.writerows(item)



