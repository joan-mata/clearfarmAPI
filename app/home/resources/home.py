from flask import Flask, render_template, request, url_for, redirect, session

from .. import home_bp

@home_bp.route('/', methods=('GET', 'POST'))
def home():
    '''
    First page //TODO
    
    Args:
        None
    '''

    if request.method == 'POST':
        action = request.form["action"]
        if action == 'search':
            return redirect(url_for('search.searches'))
        elif action == 'insert':
            if 'user' in session:
                if session['rol'] == "compute" or session['rol'] == "admin" or session['rol'] == "superadmin":
                    return redirect(url_for('inserts.farmPOST'))
            else:
                return redirect(url_for('auth.login'))

    return render_template('home/index.html')
