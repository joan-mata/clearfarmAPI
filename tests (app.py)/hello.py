from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/db")
def conectDB():
    client = MongoClient('localhost', 27017)
    db = client.flask_db
    todos = db.todos
    return "<p> Connect </p>"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
    
    
@app.route("/get")
def get():
    pass
