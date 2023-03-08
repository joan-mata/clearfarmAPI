from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db_cows

def searchLastFarm(farmID):
    '''
    Search LAST information about ONE farm
    
    Args:
        None
    '''
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db_cows["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]

        temporalData = list(db_cows[itemCollection].find({"farmID": farmID}).sort("$natural", -1))
        if temporalData:
            data.append(temporalData[0])
    
    if data:
        html = 'prints/printLastFarm.html'
    else:
        html = 'prints/printFarmEmpty.html'

    return html, data
