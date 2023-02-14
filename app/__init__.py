from flask import Flask, session
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_users = client.users

#db = client["cows"] #real cows
db = client["tests"] #pruebas
#UPLOAD_FOLDER = '/Users/joanmataparraga/Downloads'
#UPLOAD_FOLDER = '/Users/joanmataparraga/Library/Mobile Documents/com~apple~CloudDocs/Trabajo/UAB/FarmWork/clearfarm/data'

UPLOAD_FOLDER = '/home/joanmata/clearfarm/data'


def create_app():
    #ALLOWED_EXTENSIONS = set(['csv', 'json'])

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "abcd1234"
    if __name__ == '__main__':
        app.run(host='52.188.228.36',port=80)
    #db.init_app(app)

    # Registro de los Blueprints
    from .home import home_bp
    app.register_blueprint(home_bp)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .inserts import inserts_bp
    app.register_blueprint(inserts_bp)

    from .search import search_bp
    app.register_blueprint(search_bp)
        
    return app

