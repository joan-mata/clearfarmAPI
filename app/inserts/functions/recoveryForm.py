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
    elif animals == "pigs":
        db = db_pigs
    else:
        db = "error"
    
    processEnterpriseResults.processEnterpriseResults(enterprise, key)
    
    return enterprise, db
