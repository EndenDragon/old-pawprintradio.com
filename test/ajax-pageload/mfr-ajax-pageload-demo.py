#!/usr/bin/env python
from flask import Flask, render_template
import json
import urllib2

app = Flask(__name__)

response = urllib2.urlopen('http://radio.mane-frame.com/status-json.xsl')
xsl = response.read()
mfr_json = json.loads(xsl)
mfr_json = mfr_json["icestats"]["source"]
mfr_json.pop()
mfr_json = mfr_json.pop()

@app.route('/')
def index():  
    return render_template('header.html', title='index') + render_template('menu.html', menubarhomeactive='active') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content1')
def content1():
    return render_template('header.html', title='content1') + render_template('menu.html', menubarcontent1active='active') + render_template('content1.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content2')
def content2():
    return render_template('header.html', title='content2') + render_template('menu.html', menubarcontent2active='active') + render_template('content2.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content3')
def content3():
    return render_template('header.html', title='content3') + render_template('menu.html', menubarcontent3active='active') + render_template('content3.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/update_radio_subtxt')
def update_radio_subtxt():
    return "<strong>Currently playing: </strong>" + str(mfr_json["title"]) + " - <strong>Currently viewing: </strong>" + str(mfr_json["listeners"])
    #return "test"

if __name__ == "__main__":
    app.debug = True
    app.host = '0.0.0.0'
    app.run()