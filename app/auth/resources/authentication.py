from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from .. import auth_bp
from app import db

@auth_bp.route('/authentication', methods=['POST'])
def authentication():
    '''
    How identified each user for this properly function in database
    
    Args:
        None
    '''
    
    if request.method=='POST':
        user = request.form['user']
        pw = request.form['pw']
        
        encrip = hashlib.sha256(pw.encode()).digest()
        encrip = pw #TODO: Borrar, para que encripte
        
        data = list(db['users'].find({"$and":[{"user":user}, {"password": encrip}]}))

        if data:
            flag = data[0]
            #if user == flag["user"] and pw == flag["password"]:
            session['user'] = user
            session['rol'] = flag['rol']
            return redirect(url_for('home.home'))
        else:
            #BORRAR
            #session['user'] = user
            #session['rol'] = "superadmin"
            #return redirect(url_for('home.home'))
            return "User or password not correct"
            
    else:
        return "Not allow"
