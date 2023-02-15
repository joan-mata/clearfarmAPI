from flask import Flask, session
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
#db_users = client.users
#TODO: BORRAR!
db = "null"

db_cows = client["tests"]
#db_cows = client["cows"] real cows
db_pigs = client["pigs"] #real pigs
db_users = client["users"] #real users

UPLOAD_FOLDER = '/home/azureuser/clearfarmAPI/data'


def create_app():
    #ALLOWED_EXTENSIONS = set(['csv', 'json'])

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "abcd1234"
    
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

