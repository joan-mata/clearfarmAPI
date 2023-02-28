from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from . import processEnterpriseResults
from .. import inserts_bp
from app import db_cows, db_pigs

def recoveryForm():
    enterprise = request.form["collections"]
    animals = request.form["animals"]
    key = request.form["keys"]
                    
    if animals == "cows":
        db = db_cows
        processEnterpriseResults.processEnterpriseResults(db, enterprise, key)

    elif animals == "pigs":
        db = db_pigs
        processEnterpriseResults.processEnterpriseResults(db, enterprise, key)

    else:
        print("Error, No deberias estar aquí")
        #No se trata esto
        db = "error"
        
    return enterprise, db
