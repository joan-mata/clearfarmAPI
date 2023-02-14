from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db

@search_bp.route('/searchCowForm')
def searchCowForm():
    '''

    Args:
        None
    '''
    if 'user' in session:
        return render_template('search/searchCowForm.html')
    else:
        return "Error rol"
        
