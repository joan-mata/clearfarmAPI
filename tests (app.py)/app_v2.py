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
db = client.clearfarm
todos = db.todos #borrar!!
#collections (una por grupo)
#connecterra
#vet
#¿¿smarthealt??

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

    return render_template('authentication.html')

@app.route('/farmPOST', methods=('GET', 'POST'))
def farmPOST():
    print(request.method)
    if request.method == 'POST':
        file = request.files['csv_file']
        print("qa")
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            read_uploaded_file()

    return render_template('farmPOST.html')
    

def read_uploaded_file():
    filename = secure_filename(request.args.get('filename'))
    try:
        if filename and allowed_filename(filename):
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                return f.read()
    except IOError:
        pass
    return "Unable to read file"
    
def pruebaPOST1():
	if request.method=='POST' and request.form['csv_file'] != '':
	    	file_name = request.form['csv_file']
	    	f = request.files['csv_file']
	    	file_path = os.path.join(UPLOAD_FOLDER, secure_filename(f.filename))

	    	f.save(file_path)
    
    
	    	with open(file_path, 'r') as f:
	    		file_content = f.read()
	    		print(file_content)
    
