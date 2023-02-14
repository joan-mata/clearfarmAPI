from flask import Flask, render_template, request, url_for, redirect, session, send_file

import csv
import json

from . import search_bp
from app import db


@search_bp.route('/election')
def election():
    '''
    Depends the user rol, take a decision for download data or not.
    
    Args:
        None
    '''
    
    session['download'] = "No"
    if (not 'user' in session) or (session['rol'] == "farmer"):
        return redirect(url_for('search.searches'))
    else:
        return render_template('rols/computeRol.html')

@search_bp.route('/resElection', methods=['POST'])
def resElection():
    '''
    Give the answer of /election. without rol o farmer rol, can not download
    
    Args:
        None
    '''
    
    if (not 'user' in session) or (session['rol'] == "farmer"):
        session['download'] = "No"
    else:
        session['download'] = request.form['res']
    return redirect(url_for('search.searches'))
