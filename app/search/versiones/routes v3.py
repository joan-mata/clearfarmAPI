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
                    stringHtml, data = searchLastFarm(farmID)
                elif quantity == "All":
                    stringHtml, data = searchAllFarm(farmID)
                else:
                    stringHtml, data = searchRangeFarm(farmID, timeFrom, timeTo)
            else:
                if quantity == "Last":
                    stringHtml, data = searchLastCow(farmID, cowNum, id)
                elif quantity == "All":
                    stringHtml, data = searchAllCow(farmID, cowNum, id)
                else:
                    stringHtml, data = searchRangeCow(farmID, cowNum, id, timeFrom, timeTo)
                    
            if 'user' in session and session['rol'] != "farmer":
                downloadData.downloadData(data)
                flagDownload = True
                
            return render_template(stringHtml, data=data, flag=flagDownload)
        else:
            return "Error 500"

            
# Flask Searches Cow
def searchAllCow(farmID, cowNum, id):
    '''
    Search ALL information about ONE cow
    
    Args:
        None
    '''
    #find id's in reference collection
    referenceIds = list(db["reference"].find({"$and":[{"farmID": farmID},{id: cowNum}]}).sort("$natural", -1))
        
    if referenceIds:
        referenceIds = referenceIds[0]
    else:
        return 'prints/printErrorReference.html', "No information about the cow in this farm"
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]
        itemId = item["key"]

        #referenceIds values
        referenceFarmId = referenceIds["farmID"]
        referenceCowNum = referenceIds[itemId]
        
        temporalData = list(db[itemCollection].find({"$and":[{"farmID": referenceFarmId},{itemId: referenceCowNum}]}).sort("$natural", -1))
        if temporalData:
            data.append(temporalData)
            
    if data:
        html = 'prints/printAllCow.html'
    else:
        html = 'prints/printCowEmpty.html'

    return html, data

def searchLastCow(farmID, cowNum, id):
    '''
    Search LAST information about ONE cow
    
    Args:
        None
    '''
    
    #find id's in reference collection
    referenceIds = list(db["reference"].find({"$and":[{"farmID": farmID},{id: cowNum}]}).sort("$natural", -1))
            
    if referenceIds:
        referenceIds = referenceIds[0]
    else:
        return 'prints/printErrorReference.html', "No information about the cow in this farm"
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]
        itemId = item["key"]

        #referenceIds values
        referenceFarmId = referenceIds["farmID"]
        referenceCowNum = referenceIds[itemId]
        
        temporalData = list(db[itemCollection].find({"$and":[{"farmID": referenceFarmId},{itemId: referenceCowNum}]}).sort("$natural", -1))
        if temporalData:
            data.append(temporalData[0])
        
    if data:
        html = 'prints/printLastCow.html'
    else:
        html = 'prints/printCowEmpty.html'

    return html, data

def searchRangeCow(farmID, cowNum, id, timeFrom, timeTo):
    '''
    Search RANGE information about ONE cow
    
    Args:
        None
    '''
    
    #treat dates
        #Format time: YYYY-MM-DD (String)
        #Format date: [YYYY, MM, DD] (List of Int)
    dateFrom = []
    dateFrom.append(int(timeFrom[:4]))
    dateFrom.append(int(timeFrom[5:7]))
    dateFrom.append(int(timeFrom[8:]))
    
    if timeTo != "":
        dateTo = []
        dateTo.append(int(timeTo[:4]))
        dateTo.append(int(timeTo[5:7]))
        dateTo.append(int(timeTo[8:]))
    else:
        dateTo = ""
    
    #find id's in reference collection
    referenceIds = list(db["reference"].find({"$and":[{"farmID": farmID},{id: cowNum}]}).sort("$natural", -1))
            
    if referenceIds:
        referenceIds = referenceIds[0]
    else:
        return 'prints/printErrorReference.html', "No information about the cow in this farm"
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]
        itemId = item["key"]

        #referenceIds values
        referenceFarmId = referenceIds["farmID"]
        referenceCowNum = referenceIds[itemId]
        
        temporalData = list(db[itemCollection].find({"$and":[{"farmID": referenceFarmId},{itemId: referenceCowNum}]}).sort("$natural", -1))
        
        for temporalItem in temporalData:
            flag = compareDate(dateFrom, dateTo, temporalItem['date_insert_in_db'])
            
            if temporalData and flag:
                data.append(temporalItem)
    if data:
        html = 'prints/printRangeCow.html'
    else:
        html = 'prints/printRangeEmpty.html'

    return html, data

# Flask Searches Farm
def searchAllFarm(farmID):
    '''
    Search ALL information about ONE farm
    
    Args:
        None
    '''
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]

        temporalData = list(db[itemCollection].find({"farmID": farmID}).sort("$natural", -1))
        if temporalData:
            data.append(temporalData)
        
    if data:
        html = 'prints/printAllFarm.html'
    else:
        html = 'prints/printFarmEmpty.html'

    return html, data

def searchLastFarm(farmID):
    '''
    Search LAST information about ONE farm
    
    Args:
        None
    '''
        
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]

        temporalData = list(db[itemCollection].find({"farmID": farmID}).sort("$natural", -1))
        if temporalData:
            data.append(temporalData[0])
    
    if data:
        html = 'prints/printLastFarm.html'
    else:
        html = 'prints/printFarmEmpty.html'

    return html, data


def searchRangeFarm(farmID, timeFrom, timeTo):
    '''
    Search RANGE information about ONE farm
    
    Args:
        None
    '''
    #treat dates
        #Format time: YYYY-MM-DD (String)
        #Format date: [YYYY, MM, DD] (List of Int)
    dateFrom = []
    dateFrom.append(int(timeFrom[:4]))
    dateFrom.append(int(timeFrom[5:7]))
    dateFrom.append(int(timeFrom[8:]))
    
    if timeTo != "":
        dateTo = []
        dateTo.append(int(timeTo[:4]))
        dateTo.append(int(timeTo[5:7]))
        dateTo.append(int(timeTo[8:]))
    else:
        dateTo = ""
    
    #recovery collections - id matrix (list of dictionarys)
    matrix = list(db["listCollections"].find({"collection": {"$exists": "true"}}))

    data = []
    for item in matrix: #each item is a dictionary
        #item values
        itemCollection = item["collection"]
        
        temporalData = list(db[itemCollection].find({"farmID": farmID}).sort("$natural", -1))
        
        for temporalItem in temporalData:
            flag = compareDate(dateFrom, dateTo, temporalItem['date_insert_in_db'])
            
            if temporalData and flag:
                data.append(temporalItem)
    if data:
        html = 'prints/printRangeFarm.html'
    else:
        html = 'prints/printRangeEmpty.html'

    return html, data


#Compare Date functions
def compareDateFrom(date, temporal):
    '''
    Compare two dates and return True if date is previous temporal
    
    Args:
        date: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
        temporal: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
    '''
    #Analize Year
    if date[0] < temporal[0]:
        flag = True
    elif date[0] == temporal[0]:
        #Analize Month
        if date[1] < temporal[1]:
            flag = True
        elif date[1] == temporal[1]:
            #Analize Day
            if date[2] <= temporal[2]:
                flag = True
            else:
                flag = False
        else:
            flag = False
    else:
        flag = False
    return flag
 
def compareDateTo(date, temporal):
    '''
    Compare two dates and return False if date is previous temporal

    Args:
        date: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
        temporal: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
    '''
    
    #Analize Year
    if date[0] < temporal[0]:
        flag = False
    elif date[0] == temporal[0]:
        #Analize Month
        if date[1] < temporal[1]:
            flag = False
        elif date[1] == temporal[1]:
            #Analize Day
            if date[2] < temporal[2]:
                flag = False
            else:
                flag = True
        else:
            flag = True
    else:
        flag = True
    return flag
    
    
def compareDate(dateFrom, dateTo, stringDate):
    '''
    Compare thre dates and return True if stringDate is between dateFrom and dateTo. DateFrom is previous than dateTo.
    
    Args:
        dateFrom: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
        dateTo: list of 3 ints (year, month, day) -> format [YYYY, MM, DD]
        stringDate: string -> format YYYY-DD-MM
    '''
    temporalDate = []
    temporalDate.append(int(stringDate[:4]))
    temporalDate.append(int(stringDate[5:7]))
    temporalDate.append(int(stringDate[8:]))
    
    flag = compareDateFrom(dateFrom, temporalDate)
    
    if dateTo != "" and flag:
        flag = compareDateTo(dateTo, temporalDate)
        
    return flag

def downloadData(data):
    csvFilePath = 'app/downloads/csv/dataDownload.csv'
    jsonFilePath = 'app/downloads/dataDownload.json'

#    with open(csvFilePath, 'w', encoding='utf-8') as csvfile:
#        csvfile.write(json.dumps(data, indent=4))

    dataJsonObj = json.loads(json_util.dumps(data))

    #upload JSON file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsfile:
        json.dump(dataJsonObj, jsfile, indent=4)
    
    #upload CSV files
    iteration = 1
    csvAuxPath = csvFilePath[:-4]
    for item in dataJsonObj:
        csvEndPath = csvAuxPath + str(iteration) + '.csv'
        iteration += 1
        
        df = pd.json_normalize(item)
        df.to_csv(csvEndPath)


#        with open(csvEndPath, 'w') as f:
#            wr = csv.DictWriter(f, fieldnames = item[0].keys())
#            wr.writeheader()
#            wr.writerows(item)







