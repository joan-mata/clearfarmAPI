from flask import Flask, render_template, request, url_for, redirect, session

import hashlib

from .. import auth_bp
from app import db

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
