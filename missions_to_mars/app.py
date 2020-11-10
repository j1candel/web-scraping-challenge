from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo 


app = Flask(__name__)

app.config['PyMongo'] ='mongodb://localhost:27017'
mongo = PyMongo(app)

@app.route('/')
def index
