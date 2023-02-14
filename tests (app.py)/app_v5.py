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

#db_cows = client["cows"] #real cows
db_cows = client["tests"] #pruebas

#functions

def insertEnterprise(csvFilePath):
    data = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        date = datetime.today().strftime('%Y-%B-%d %H:%M')
        dict = {'date insert in db': date}

        for rows in csvReader:
            key = {}
            key.update(dict)
            key.update(rows)
            data.append(key)

    return data

def insertReference(collection, csvFilePath):
    # cowID, (farmID, cowTag), official_cowID, DOB

    data = []
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        date = datetime.today().strftime('%Y-%B-%d %H:%M')
        dict = {'date insert in db': date}
        
        for rows in csvReader:
            comp = collection.find({}, {'cowID': rows['cowID'], 'farmID': rows['farmID'], 'cowTag': rows['cowTag'], 'official_cowID': rows['official_cowID'], 'DOB': rows['DOB'],})

            if comp:
                #update
                pass
            else:
                pass
                key = {}
                key.update(dict)
                key.update(rows)
                data.append(key)

    return data

def attendCollections(db, csvFile, collection):
    mycol = db[collection]

    if collection == 'reference':
        #data = insertReference(mycol,csvFile)
        data = insertEnterprise(csvFile)

    else:
        data = insertEnterprise(csvFile)
    
    mycol.insert_many(data)


#flask functions

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

        attendCollections(db_cows, csvFilePath, enterprise)

        #return redirect(url_for('home'))

    return render_template('farmPOST.html')

