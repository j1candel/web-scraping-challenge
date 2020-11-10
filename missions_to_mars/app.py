from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

@app.route('/')
def index():

    mars_dict = mongo.db.mars_dict.find_one()

    return render_template('index.html', mars = mars_dict)

if __name__ == "__main__":
    app.run(debug=True)
