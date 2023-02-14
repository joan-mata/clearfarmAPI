from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
import csv
import json
from werkzeug.utils import secure_filename


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos


def CSVtoJSON(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        data['0'] = {'date': datetime.today().strftime('%Y-%B-%d %H:%M')}
        key = 1
        for rows in csvReader:
            data[key] = rows
            key += 1

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.args.get('search'):
        search = request.args.get('search')
        data = []
#            answers = db.todos.find({ 'date': { '$exists': 'true' }})
        listElements = list(db.todos.find())
        for block in listElements:
            for item in block:
                try:
                    if search in block[item]:
                        print(block[item][search])
                        data.append("<p>" + str(block[item]) + " </p>")
                except:
                    pass
        return "<p>" + str(data) + " </p>"

    if request.method=='POST':
        return redirect(url_for('authentication'))
    
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.route('/authentication', methods=('GET', 'POST'))
def authentication():
    if request.method=='POST':
        #TODO -> cambiar comprobacion por una clave publica ¿como?
        user = request.form['user']
        pw = request.form['pw']
        if user == 'joan' and pw == '1234':
            return redirect(url_for('farmPOST'))

    all_todos = todos.find()
    return render_template('authentication.html', todos=all_todos)

@app.route('/farmPOST', methods=('GET', 'POST'))
def farmPOST():
    if request.method=='POST' and request.form['csv_file'] != '':
#        f = request.files['csv_file'] #TODO -> como recoger la info del documento cargado ¿?
#        csvFile = f.filename
#        f.save(secure_filename(csvFile))
        #csvFilePath = open ('csvFile.csv', "r")#Este documento esta en la app ¡!
        csvFilePath = r'csvFile.csv' #Este documento se reescribe
        jsonFilePath = r'file.json' #Este documento se reescribe
        CSVtoJSON(csvFilePath, jsonFilePath)
        
        with open(jsonFilePath) as f1:
            file_data = json.load(f1)
            
        todos.insert_one(file_data)
        return redirect(url_for('home'))

    all_todos = todos.find()
    return render_template('farmPOST.html', todos=all_todos)
