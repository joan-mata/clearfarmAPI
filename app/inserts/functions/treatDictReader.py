from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os
import hashlib

from . import recoveryPreviousHash
from .. import inserts_bp
from app import db, UPLOAD_FOLDER

def treatDictReader(csvf):
    data = []

    csvReader = csv.DictReader(csvf)

    #add date from today
    date = datetime.today().strftime('%Y-%m-%d')
    dict = {'date_insert_in_db': date}
    hashPrevious = recoveryPreviousHash.recoveryPreviousHash(db[enterprise])

    for rows in csvReader:
        key = {}
        key.update(dict)
        key.update(hashPrevious)        
        key.update(rows)
        hash, hashPrevious = computeHash.computeHash(key)
        key.update(hash)
        data.append(key)

    return data

