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
    data = list(dataBase.find({"hash": {"$exists": "true"}}).sort("$natural", -1))
    dict = {'hash_previous': str(data[0])}
    return dict


