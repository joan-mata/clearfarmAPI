from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp

@search_bp.route('/downloadCSV')
def downloadCSV():
    '''
    Download the data file at the user
    
    Args:
        None
    '''
    
    if 'user' in session and session['rol'] != "farmer":
        PATH='downloads/csv'
        FILE='dataDownload.csv'
        return send_from_directory(PATH,FILE,as_attachment=True)
        #return send_file(PATH,as_attachment=True)
    else:
        return "Not possible to access"
    
