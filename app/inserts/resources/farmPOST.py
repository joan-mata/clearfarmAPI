from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from .. import inserts_bp
from app import db_cows, db_pigs, UPLOAD_FOLDER
from ..functions import recoveryForm
from ..functions import treatListReader


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
            data = treatListReader.treatListReader(csvf, db, enterprise)

        db[enterprise].insert_many(data)
        return data

    return render_template('inserts/farmPOST.html')

