from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from .. import inserts_bp
from app import db, UPLOAD_FOLDER

def recoveryPreviousHash(dataBase):
    data = list(dataBase.find({}, {"hash": 1}).sort("$natural", -1))
    
    print('Data: ' + str(data))

    if data:
        print('Data[0]: ' + str(data[0]))
        dict_aux = data[0]
        print('Dict_aux["hash"]: ' + str(dict_aux["hash"]))
        dict = {'hash_previous': str(dict_aux["hash"])}
    else:
        dict = {'hash_previous': '0'}

    return dict


