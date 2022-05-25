from app import app
from flask import render_template
import requests as r
from .services import getRegions,getCities,getCrypto

@app.route('/')
def home():
    cities = getCities()
    regions = getRegions()
    return render_template('index.html',regions = regions, cities = cities)

@app.route('/about')
def about():
    crypto= getCrypto()
    return render_template('about.html',crypto = crypto)

@app.route('/lists')
def lists():
    cities = getCities()
    crypto = getCrypto()
    return render_template('lists.html',cities = cities,**crypto)
