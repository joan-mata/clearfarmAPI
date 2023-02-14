from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from . import inserts_bp
from app import db

@inserts_bp.route('/farmPOST', methods=('GET', 'POST'))
def farmPOST():
    '''
    Insert farm's data in DBxw
    
    Args:
        None
    '''
    
    if request.method=='POST': #and request.form['csv_file'] != '':
        enterprise = request.form["collections"]

        csvFilePath = r'data/' + enterprise + '.csv'
        
        #TODO: no va, solo cuando existe en listCollections
        count = db['listCollections'].count_documents({"collection": enterprise})
        
        if count == 0:
            if enterprise != "reference" and enterprise != "matComp":
                key = request.form["keys"]
                db['listCollections'].insert({"collection": enterprise, "key": key})
        
        data = []
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            #add date from today
            date = datetime.today().strftime('%Y-%m-%d')
            dict = {'date_insert_in_db': date}
            for rows in csvReader:
                key = {}
                key.update(dict)
                key.update(rows)
                data.append(key)
        
        db[enterprise].insert_many(data)
        return redirect(url_for('home.home'))

    return render_template('inserts/farmPOST.html')

