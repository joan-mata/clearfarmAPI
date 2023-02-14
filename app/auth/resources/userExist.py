from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from .. import auth_bp
from app import db

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
