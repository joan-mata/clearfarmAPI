from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db
from . import compareDate

def searchRangeFarm(farmID, timeFrom, timeTo):
    '''
    Search RANGE information about ONE farm
    
    Args:
        None
    '''
    #treat dates
        #Format time: YYYY-MM-DD (String)
        #Format date: [YYYY, MM, DD] (List of Int)
    dateFrom = []
    dateFrom.append(int(timeFrom[:4]))
    dateFrom.append(int(timeFrom[5:7]))
    dateFrom.append(int(timeFrom[8:]))
    
    if timeTo != "":
        dateTo = []
        dateTo.append(int(timeTo[:4]))
        dateTo.append(int(timeTo[5:7]))
        dateTo.append(int(timeTo[8:]))
    else:
        dateTo = ""
    
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]
        
        temporalData = list(db[itemCollection].find({"farmID": farmID}).sort("$natural", -1))
        
        for temporalItem in temporalData:
            flag = compareDate.compareDate(dateFrom, dateTo, temporalItem['date_insert_in_db'])
            
            if temporalData and flag:
                data.append(temporalItem)
    if data:
        html = 'prints/printRangeFarm.html'
    else:
        html = 'prints/printRangeEmpty.html'

    return html, data

