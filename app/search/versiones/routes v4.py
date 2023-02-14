from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from . import search_bp
from app import db
from . import downloadData

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
        

@search_bp.route('/searchCowData', methods=['POST'])
def searchCowData():
    '''
    Treath the answers of Cow Form
    
    Args:
        None
    '''
    if not 'user' in session:
        return "Error rol"
    else:
        if request.method=='POST':
            farmID = request.form['farmID']
            cowNum = request.form['cowNum']
            id = request.form['ID']
            quantity = request.form['quantity']
            timeFrom = request.form['timeFrom']
            timeTo = request.form['timeTo']
            
            flagDownload = False
            
            if timeFrom != "":
                quantity = "Range"
            
            if cowNum == "":
                if quantity == "Last":
                    stringHtml, data = searchLastFarm.searchLastFarm(farmID)
                elif quantity == "All":
                    stringHtml, data = searchAllFarm.searchAllFarm(farmID)
                else:
                    stringHtml, data = searchRangeFarm.searchRangeFarm(farmID, timeFrom, timeTo)
            else:
                if quantity == "Last":
                    stringHtml, data = searchLastCow.searchLastCow(farmID, cowNum, id)
                elif quantity == "All":
                    stringHtml, data = searchAllCow.searchAllCow(farmID, cowNum, id)
                else:
                    stringHtml, data = searchRangeCow.searchRangeCow(farmID, cowNum, id, timeFrom, timeTo)
                    
            if 'user' in session and session['rol'] != "farmer":
                downloadData.downloadData(data)
                flagDownload = True
                
            return render_template(stringHtml, data=data, flag=flagDownload)
        else:
            return "Error 500"

            
