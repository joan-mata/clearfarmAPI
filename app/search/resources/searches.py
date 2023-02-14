from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from app import db

@search_bp.route('/searches', methods=('GET', 'POST'))
def searches():
    '''
    Select what search I want
    
    Args:
        None
    '''
    if request.method=='POST':
        action = request.form['searches']
        if action == 'cow':
            return redirect(url_for('search.searchCowForm'))
        elif action == 'other':
            pass
        #messages.warning(request, 'Clica en una opción válida.')

    return render_template('search/searches.html')
