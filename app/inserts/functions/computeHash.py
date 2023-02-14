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

def computeHash(key):
    hash = hashlib.sha256(str(key).encode()).digest()
    dict = {'hash': hash}
    return dict

