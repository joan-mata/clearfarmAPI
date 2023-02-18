from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os
import hashlib

from .. import inserts_bp
from app import db, UPLOAD_FOLDER

def treatListReader(csvf):
    data = []

    csvReader_semicolon = csv.reader(csvf, delimiter=';')
    csvReader_comma = csv.reader(csvf)
    
    print("csvReader_semicolon :" + str(csvReader_semicolon))
    print("csvReader_semicolon type:" + str(type(csvReader_semicolon)))
    print("csvReader_comma :" + str(csvReader_comma))
    print("csvReader_comma type:" + str(type(csvReader_comma)))

    if csvReader_semicolon[0] > csvReader_comma[0]:
        csvReader = csvReader_semicolon
        headers = csvReader_semicolon[0]

    else:
        csvReader = csvReader_comma
        headers = csvReader_comma[0]
    
    #add date from today
    date = datetime.today().strftime('%Y-%m-%d')
    dict = {'date_insert_in_db': date}
    hashPrevious = recoveryPreviousHash.recoveryPreviousHash(db[enterprise])
    
    for i in range(1, len(csvReader)):
    #for rows in csvReader:
        key = {}
        key.update(dict)
        key.update(hashPrevious)

#        print("---- NEW ITEM ----")
#        print("Rows:" + str(rows))
#        print("Rows type:" + str(type(rows)))
#        print("Rows list:" + str(list(rows)))
#
        update_rows = {}

#        print("Rows.keys():" + str(rows.keys()))
#        print("Rows.values():" + str(rows.values()))

        for tupla in zip(headers, csvReader[i]):
#            print("tupla_key:" + str(tupla[0]))
#            print("tupla_key type:" + str(type(tupla[0])))
#            print("tupla_value:" + str(tupla[1]))
#            print("tupla_value type:" + str(type(tupla[1])))
#            print("...")

            if tupla[1] != "":
                dict_aux = {str(tupla[0]): str(tupla[1])}
                update_rows.update(dict_aux)

        key.update(update_rows)

        
        
#        key.update(rows)
        
        
        
        hash, hashPrevious = computeHash.computeHash(key)
        data.append(key)
        
        
    return data

