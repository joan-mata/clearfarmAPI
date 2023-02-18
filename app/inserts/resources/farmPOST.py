from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from .. import inserts_bp
from app import db_cows, db_pigs, UPLOAD_FOLDER
from ..functions import computeHash
from ..functions import recoveryForm
from ..functions import recoveryPreviousHash


@inserts_bp.route('/farmPOST', methods=('GET', 'POST'))
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
                
        data = []
        with open(csvFilePath, encoding='utf-8') as csvf:
            #dialect = csv.Sniffer(delimiters=";").sniff(csvf.read(1024)) #probar
            csvReader = csv.reader(csvf, delimiter=';')
            #csvReader = csv.reader(csvf, dialect='semicolon')
            #DictReader(csvf) #probar semicolon
            #add date from today
            date = datetime.today().strftime('%Y-%m-%d')
            dict = {'date_insert_in_db': date}
            hashPrevious = recoveryPreviousHash.recoveryPreviousHash(db[enterprise])

            for rows in csvReader:
                key = {}
                key.update(dict)
                key.update(hashPrevious)


#                print("---- NEW ITEM ----")
#                print("Rows:" + str(rows))
#                print("Rows type:" + str(type(rows)))
#                print("Rows list:" + str(list(rows)))
#
#                update_rows = {}
#
#                print("Rows.keys():" + str(rows.keys()))
#                print("Rows.values():" + str(rows.values()))
#
#                for tupla in zip(list(rows.keys()), list(rows.values())):
#                    print("tupla_key:" + str(tupla[0]))
#                    print("tupla_key type:" + str(type(tupla[0])))
#                    print("tupla_value:" + str(tupla[1]))
#                    print("tupla_value type:" + str(type(tupla[1])))
#                    print("...")
#
#                    if tupla[1] != "":
#                        dict_aux = {str(tupla[0]): str(tupla[1])}
#                        update_rows.update(dict_aux)
#
#                key.update(update_rows)
                
                
                
                key.update(rows)
                
                
                
                hash, hashPrevious = computeHash.computeHash(key)
                data.append(key)

        db_cows[enterprise].insert_many(data)
        return redirect(url_for('home.home'))

    return render_template('inserts/farmPOST.html')

