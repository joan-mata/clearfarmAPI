from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

UPLOAD_FOLDER = 'C./home/joanmata/clearfarm/filedata'
ALLOWED_EXTENSIONS = set(['csv', 'json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('localhost', 27017)
db_users = client.users
#db_cows = client.cows #real
db_cows = client.tests #pruebas


def CSVtoJSON(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        date = datetime.today().strftime('%Y-%B-%d %H:%M')
        key = 1
        for rows in csvReader:
            data[key] = rows
            key += 1

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        action = request.form["action"]
        if action == 'search':
            pass
        elif action == 'insert':
            return redirect(url_for('authentication'))

    return render_template('index.html')


@app.route('/authentication', methods=('GET', 'POST'))
def authentication():
    if request.method=='POST':
        #TODO: cifrar password
        user = request.form['user']
        pw = request.form['pw']
        if user == 'joan' and pw == '1234':
            #db.auth("joanmata", passwordPrompt())
            return redirect(url_for('farmPOST'))

    return render_template('authentication.html')

@app.route('/farmPOST', methods=('GET', 'POST'))
def farmPOST():
    if request.method=='POST' and request.form['csv_file'] != '':
        enterprise = request.form["collections"]

        csvFilePath = r'filedata/' + enterprise + '.csv' 
        #csvFilePath = r'filedata/reference.csv' 

        jsonFilePath = r'filedata/file.json' #Este documento se reescribe
        CSVtoJSON(csvFilePath, jsonFilePath)
        
        with open(jsonFilePath) as f1:
            file_data = json.load(f1)

        insertCollection(db_cows, file_data, enterprise)
        #db_cows.reference.insert_one(file_data)

        return redirect(url_for('home'))

    return render_template('farmPOST.html')

def insertCollection(db, file, collection):
    if collection == "connectTerra":
        db.connectTerra.insert_one(file)
    elif collection == "vet":
        db.vet.insert_one(file)
    elif collection == "smarxTec":
        db.smarxTec.insert_one(file)
    elif collection == "covap":
        db.covap.insert_one(file)
    elif collection == "herdItt":
        db.herdItt.insert_one(file)