from flask import Flask, render_template, request, url_for, redirect, session, send_file, send_from_directory
from bson import json_util

import csv
import json
import pandas as pd

from .. import search_bp

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
