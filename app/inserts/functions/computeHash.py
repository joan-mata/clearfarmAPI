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
    hash_actual = {'hash': str(hash)}
    hash_previous = {'hash_previous': str(hash)}
    return hash_actual, hash_previous

