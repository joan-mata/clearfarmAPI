from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from . import auth_bp
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
            return "User or password not correct"
            
    else:
        return "Not allow"

@auth_bp.route('/signup')
def signup():
    if 'user' in session and session['rol'] == "superadmin":
        return render_template('auth/signup.html')
    else:
        return "Error"
    
@auth_bp.route('/userExist', methods=['POST'])
def userExist():
    if 'user' in session and session['rol'] == "superadmin":
        pw = request.form['pw']
        confirm = request.form['confirm']
            
        if pw == confirm:
            #TODO: confirmar que no existe en la db
            encrip = hashlib.sha256(pw.encode()).digest()
            user = request.form['user']
            rol = request.form['rol']
            dict = {'user': user, 'password': encrip, 'rol': rol}
            data = [dict]
            db['users'].insert_many(data)
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('auth.signup'))
    else:
        return "Error"

@auth_bp.route('/login')
def login():
    if not 'user' in session:
        return render_template('auth/login.html')
    else:
        return "Already login"


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
