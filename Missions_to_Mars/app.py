# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)