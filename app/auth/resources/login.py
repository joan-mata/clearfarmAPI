from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from .. import auth_bp
from app import db

@auth_bp.route('/login')
def login():
    if not 'user' in session:
        return render_template('auth/login.html')
    else:
        return "Already login"
