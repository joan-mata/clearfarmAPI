from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db

@search_bp.route('/downloadJSON')
def downloadJSON():
    '''
    Download the data file at the user
    
    Args:
        None
    '''
    if 'user' in session and session['rol'] != "farmer":
        PATH='downloads/dataDownload.json'
        return send_file(PATH,as_attachment=True)
    else:
        return "Not possible to access"
    
