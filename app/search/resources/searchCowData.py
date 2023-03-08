from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp
from ..functions import compareDate
from ..functions import downloadData
from ..functions import searchAllCow
from ..functions import searchAllFarm
from ..functions import searchLastCow
from ..functions import searchLastFarm
from ..functions import searchRangeCow
from ..functions import searchRangeFarm

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
                    stringHtml, data = searchLastFarm.searchLastFarm(farmID)
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

            
