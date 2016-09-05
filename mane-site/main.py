from flask import Flask, render_template, request, jsonify, abort
from xml2dict import ElementTree, XmlListConfig, XmlDictConfig
from crossdomainfuncs import crossdomain
from string import printable
import urllib2
import json
import commands
import os
import time
import datetime
import math
import re
import logging
import HTMLParser
import subprocess
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
os.environ['TZ'] = 'America/Los_Angeles'
gitRevision = commands.getoutput("git rev-parse --short master")
os.chdir(os.path.dirname(os.path.realpath(__file__)))
app.wsgi_app = ProxyFix(app.wsgi_app)

def file_get_contents(filename):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename) as f:
        return f.read()

def fix_ascii(string):
    ''' Returns the string without non ASCII characters'''
    return u'{0}'.format(string)

def getMFRTumblr():
    response = urllib2.urlopen('http://maneframeradio.tumblr.com/api/read?start=0&num=10')
    html = response.read()
    root = ElementTree.XML(html)
    xmldict = XmlDictConfig(root)
    xmldict = xmldict["posts"]
    t = xmldict["post"]
    posts = []
    for x in t:
        if x['type'] == "regular":
            try:
                regTitle = x["regular-title"]
            except:
                regTitle = "Post"
            regBody = x["regular-body"]
        if x['type'] == "photo":
            a = ""
            try:
                for m in x['photoset']['photo']:
                    a = '<img src="' + m[1] + '">' + a
            except:
                img = html[html.find('<photo-url max-width="500">', html.find(x['id']))+27:html.find('</photo-url>', html.find('<photo-url max-width="500">', html.find(x['id'])))]
                a = '<img src="' + img + '">'
            try:
                a = a + x["photo-caption"]
            except:
                pass
            regTitle = "Photo"
            regBody = a
        if x['type'] == "link":
            link_text = x['link-text']
            link_url = x['link-url']
            link_desc = x['link-description']
            regTitle = "Link"
            regBody = '<a href="' + link_url + '">' + link_text + "</a> <small>(" + link_url + ")</small>" + link_desc
        if x['type'] == "quote":
            regTitle = "Quote"
            quote_txt = x['quote-text']
            quote_src = x['quote-source']
            regBody = '<blockquote><p>' + quote_txt + '</p><br><small style="color: white;">' + quote_src + '</small></blockquote>'
        if x['type'] == "conversation":
            regTitle = x['conversation-title']
            regBody = x['conversation-text']
        if x['type'] == "audio":
            regTitle = x['id3-title']
            audioContent = x['audio-embed']
            caption = x['audio-caption']
            regBody = audioContent + caption
        if x['type'] == "video":
            video_player = html[html.find('<video-player max-width="500">', html.find(x['id']))+31:html.find('</video-player>', html.find('<video-player max-width="500">', html.find(x['id'])))]
            video_player = HTMLParser.HTMLParser().unescape(video_player)
            video_player = video_player[:6] + " controls" + video_player[7:]
            regTitle = "Video"
            regBody = video_player + x['video-caption']
        a = {'title': regTitle, 'url': x["url"], 'timestamp': x["date"], 'content': regBody}
        posts.append(a)
        regTitle = "ERROR"
        regBody = "ERROR"
    return posts

def getReqSongs(count=False):
    config_file = file_get_contents("config.json")
    config_file = json.loads(config_file)
    songListEndpoint = config_file["requestsListURL"]
    response = urllib2.urlopen(songListEndpoint).read()
    response = json.loads(response)["result"]
    if count:
        return len(response)
    return response

def submitReqSong(id):
    config_file = file_get_contents("config.json")
    config_file = json.loads(config_file)
    songListEndpoint = config_file["requestsSubmitURL"]
    response = urllib2.urlopen(songListEndpoint+str(id)).read()
    response = json.loads(response)
    if response["status"] == "success":
        return {'status': True}
    return {'status': False, 'error': response["error"]}

@app.route('/')
def index():
    t = getMFRTumblr()[0]
    postContent = t["content"]
    postURL = t["url"]
    postTimestamp = t["timestamp"]
    postTitle = t["title"]
    return render_template('header.html', title="Welcome") + render_template('menu.html', animatedMenubar="animated fadeInDown") + render_template('index.html', postTitle = postTitle, postContent = postContent, postURL = postURL, postTimestamp = postTimestamp) + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/about')
def about():
    return render_template('header.html', title="About") + render_template('menu.html', activeAbout="active") + render_template('about.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/blog')
def blog():
    posts = getMFRTumblr()
    return render_template('header.html', title="Blog") + render_template('menu.html', activeBlog="active") + render_template('blog.html', posts=posts) + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/events')
def events():
    return render_template('header.html', title="Events") + render_template('menu.html', activeEvents="active") + render_template('events.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/team')
def team():
    return render_template('header.html', title="Team") + render_template('menu.html', activeTeam="active") + render_template('team.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/partners')
def partners():
    return render_template('header.html', title="Partners") + render_template('menu.html', activePartners="active") + render_template('partners.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/contact')
def contact():
    return render_template('header.html', title="Contact") + render_template('menu.html', activeContact="active") + render_template('contact.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/update_radio_subtxt', methods=['GET'])
@crossdomain(origin='*')
def update_radio_subtxt():
    response = urllib2.urlopen('https://radio.pawprintradio.com/api/nowplaying/index/1')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json['result'][0]
    curr_song = mfr_json['current_song']
    listeners = mfr_json['listeners']
    return fix_ascii(curr_song['text']) + " <em>" + str(listeners["current"]) + "</em>"

@app.route('/update_radio_subtxt/json', methods=['GET'])
@crossdomain(origin='*')
def update_radio_subtxt_json():
    response = urllib2.urlopen('https://radio.pawprintradio.com/api/nowplaying/index/1')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json['result'][0]
    curr_song = mfr_json['current_song']
    listeners = mfr_json['listeners']
    return jsonify({'text': fix_ascii(curr_song['text']), 'title': fix_ascii(curr_song['title']), 'artist': fix_ascii(curr_song['artist']), 'listeners': listeners["current"]})

#Begin Requests system
@app.route("/requests")
def requests():
    t = str(getReqSongs(count=True))
    return render_template('requestChoose.html', paginations=math.ceil((float(str(t))/25)))

@app.route("/getTable/<index>")
def getTable(index):
    t = getReqSongs()
    m = ""
    t = t[(int(float(index)) - 1) * 25:(int(float(index)) - 1)*25+25]
    for x in t:
        m = m + "<tr>" + "<td>" + fix_ascii(x["request_song_id"]) + "</td>" + "<td>" + fix_ascii(x["song"]["artist"]) + "</td>" + "<td>" + fix_ascii(x["song"]["title"]) + "</td>" + '''<td><a href="reqForm/''' + fix_ascii(x["request_song_id"]) + '''"><button type="button">Request Song</button></a></td>''' + "</tr>"
    return '<table border="1" style="width:100%"><tr style="font-size: 30px;"><td>ID</td><td>Artist</td><td>Title</td><td>Action</td></tr><br>' + m + "</table>"

@app.route("/searchTable/<query>")
def searchTable(query):
    t = getReqSongs()
    m = ""
    for x in t:
        if query.lower() in x["song"]["title"].lower() or query.lower() in x["song"]["artist"].lower():
            m = m + "<tr>" + "<td>" + fix_ascii(x["request_song_id"]) + "</td>" + "<td>" + fix_ascii(x["song"]["artist"]) + "</td>" + "<td>" + fix_ascii(x["song"]["title"]) + "</td>" + '''<td><a href="reqForm/''' + fix_ascii(x["request_song_id"]) + '''"><button type="button">Request Song</button></a></td>''' + "</tr>"
    return '<table border="1" style="width:100%"><tr style="font-size: 30px;"><td>ID</td><td>Artist</td><td>Title</td><td>Action</td></tr><br>' + m + "</table>"

@app.route("/reqForm/<songid>")
def requestForm(songid):
    t = getReqSongs()
    reqID = ""
    reqTITLE = ""
    reqARTIST = ""
    for x in t:
        if int(float(songid)) == int(float(x["request_song_id"])):
            reqID = fix_ascii(x["request_song_id"])
            reqTITLE = fix_ascii(x["song"]["title"])
            reqARTIST = fix_ascii(x["song"]["artist"])
    return render_template('requestForm.html', reqID=reqID, reqTITLE=reqTITLE, reqARTIST=reqARTIST)

@app.route("/request-post", methods=['POST'])
def request_post():
    t = getReqSongs()
    reqSONGID = request.form['reqSONGID']
    reqTITLE = ""
    reqARTIST = ""
    for x in t:
        if int(float(reqSONGID)) == int(float(x["request_song_id"])):
            reqSONGID = fix_ascii(x["request_song_id"])
            reqTITLE = fix_ascii(x["song"]["title"])
            reqARTIST = fix_ascii(x["song"]["artist"])
    post = submitReqSong(reqSONGID)
    if post['status'] == True:
        return render_template('requestConfirmation.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST)
    else:
        return render_template('requestErrorInQueue.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST, errorMESSAGE=post['error'])
#End Requests System

@app.route("/gitlabUpdate", methods=['POST'])
def gitlabUpdate():
    app_config = file_get_contents("config.json")
    app_config = json.loads(app_config)
    if request.headers.get("X-Gitlab-Token", "") == app_config["gitlabWebhookSecret"]:
        try:
            subprocess.Popen("git pull", shell=True).wait()
        except OSError:
            return "ERROR", 500
        return "OK", 200
    else:
        return "ERROR", 401

if __name__ == '__main__':
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('flask.log')
    logger.addHandler(handler)
    app_config = file_get_contents("config.json")
    app_config = json.loads(app_config)
    app.run(host=str(app_config["ip"]),port=int(float(str(app_config["port"]))),debug=app_config["debug"] in ["True","true"])
