#!/usr/bin/env python
from flask import Flask, render_template
import json
import urllib2

app = Flask(__name__)

@app.route('/')
def index():
    
    response = urllib2.urlopen('http://radio.mane-frame.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json.pop()
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return render_template('index.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"])

@app.route('/update_radio_subtxt')
def update_radio_subtxt():
    response = urllib2.urlopen('http://radio.mane-frame.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json.pop()
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return "<strong>Currently playing: </strong>" + str(mfr_json["title"]) + " - <strong>Currently viewing: </strong>" + str(mfr_json["listeners"])
    #return "test"

if __name__ == "__main__":
    app.debug = True
    app.host = '0.0.0.0'
    app.run()