from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from .. import auth_bp
from app import db

@auth_bp.route('/signup')
def signup():
    if 'user' in session and session['rol'] == "superadmin":
        return render_template('auth/signup.html')
    else:
        return "Error"
