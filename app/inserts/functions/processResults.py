from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import csv
import json
import os

from .. import inserts_bp

def processEnterpriseResults(enterprise, key):
    try: # If exist this enterprise
        db['listCollections'].count_documents({"collection": enterprise})
    except: # If not exist this enterprise
        if enterprise != "reference" and enterprise != "matComp":
            db['listCollections'].insert({"collection": enterprise, "key": key})
    
