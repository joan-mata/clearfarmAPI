from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from .. import inserts_bp
from ..functions import recoveryForm
from ..functions import treatDictReader
from ..functions import treatListReader
from ..functions import computeHash
from ..functions import recoveryPreviousHash
from app import db_cows, UPLOAD_FOLDER

@inserts_bp.route('/farmPOST', methods=['GET', 'POST'])
def farmPOST():
    '''
    Insert farm's data in DB
    
    Args:
        None
    '''
    
    if request.method=='POST':
        enterprise, db = recoveryForm.recoveryForm()

        f = request.files['csvfile']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, enterprise + '.csv'))

        csvFilePath = r'data/' + enterprise + '.csv'

        with open(csvFilePath, encoding='utf-8') as csvf:
#            data = treatDictReader.treatDictReader(csvf, db, enterprise)
            data = treatListReader.treatListReader(csvf, db, enterprise)

#        print("type: " + str(type(data)))
#        print("type element: " + str(type(data[0])))
#        print("len: " + str(len(data)))
#        print("data: " + str(data))
#        print("db: " + str(db))
#        print("enterprise: " + str(enterprise))
#
#        collection = db[enterprise]
#
#        print("collection: " + str(collection))

        collection.insert_many(data)
        return redirect(url_for('home.home'))

#        enterprise = request.form["collections"]
#
#        f = request.files['csvfile']
#        filename = secure_filename(f.filename)
#        f.save(os.path.join(UPLOAD_FOLDER, enterprise + '.csv'))
#
#        csvFilePath = r'data/' + enterprise + '.csv'
#
#        try: # If exist this enterprise
#            count = db_cows['listCollections'].count_documents({"collection": enterprise})
#        except: # If not exist this enterprise
#            count = 0
#
#        if count == 0:
#            if enterprise != "reference" and enterprise != "matComp":
#                key = request.form["keys"]
#                db_cows['listCollections'].insert_one({"collection": enterprise, "key": key})
#
#        data = []
#        with open(csvFilePath, encoding='utf-8') as csvf:
#            csvReader = csv.DictReader(csvf)
#            #add date from today
#            date = datetime.today().strftime('%Y-%m-%d')
#            dict = {'date_insert_in_db': date}
#            hashPrevious = recoveryPreviousHash.recoveryPreviousHash(db_cows[enterprise])
#
#            for rows in csvReader:
#                key = {}
#                key.update(dict)
#                key.update(hashPrevious)
#                key.update(rows)
#                hash, hashPrevious = computeHash.computeHash(key)
#                key.update(hash)
#                data.append(key)
#
#        db_cows[enterprise].insert_many(data)
#        return redirect(url_for('home.home'))

    return render_template('inserts/farmPOST.html')

