#!/usr/bin/env python
from flask import Flask, render_template
import json
import urllib2
import os

app = Flask(__name__)

def file_get_contents(filename):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename) as f:
        return f.read()

def getPlaying():
    response = urllib2.urlopen('http://radio.mane-frame.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return mfr_json

@app.route('/')
def index():  
    mfr_json = getPlaying()
    return render_template('header.html', title='index') + render_template('menu.html', menubarhomeactive='active') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content1')
def content1():
    mfr_json = getPlaying()
    return render_template('header.html', title='content1') + render_template('menu.html', menubarcontent1active='active') + render_template('content1.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content2')
def content2():
    mfr_json = getPlaying()
    return render_template('header.html', title='content2') + render_template('menu.html', menubarcontent2active='active') + render_template('content2.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/content3')
def content3():
    mfr_json = getPlaying()
    return render_template('header.html', title='content3') + render_template('menu.html', menubarcontent3active='active') + render_template('content3.html') + render_template('player.html', playing=str(mfr_json["title"]), viewers=mfr_json["listeners"]) + render_template('footer.html')

@app.route('/update_radio_subtxt')
def update_radio_subtxt():
    mfr_json = getPlaying()
    return "<strong>Currently playing: </strong>" + str(mfr_json["title"]) + " - <strong>Currently viewing: </strong>" + str(mfr_json["listeners"])
    #return "test"

if __name__ == "__main__":
    app.debug = "True" == file_get_contents("debugMode")[0:4]
    if app.debug == True:
        print "\n------------------------------\nWarning: Debug is set to TRUE. Do not use debug in live production as it poses a security issue.\nTo turn debug off, please change 'True' to 'False' in the 'debugMode' file.\n------------------------------\n"
    app.run()