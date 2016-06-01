from flask import Flask, render_template, request, jsonify, abort
from xml2dict import ElementTree, XmlListConfig, XmlDictConfig
from crossdomainfuncs import crossdomain
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import *
import urllib2
import json
import commands
import os
import MySQLdb
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

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

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

@app.route('/update_radio_subtxt', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def update_radio_subtxt():
    response = urllib2.urlopen('http://radio.pawprintradio.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return strip_non_ascii(str(mfr_json["title"])) + " <em>" + str(mfr_json["listeners"]) + "</em>"

@app.route('/json/update_radio_subtxt', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def json_update_radio_subtxt():
    response = urllib2.urlopen('http://radio.pawprintradio.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return str(json.dumps({"title": str(mfr_json["title"]), "listeners": str(mfr_json["listeners"])}))

#Begin Requests system
mysql_login = file_get_contents("mysql-login.json")
mysql_login = json.loads(mysql_login)
engine = create_engine('mysql://' + str(mysql_login["username"]) + ':' + str(mysql_login["password"]) + '@' + str(mysql_login["ip"]) + ':' + str(mysql_login["port"]) + '/' + str(mysql_login["database"]))
connection = engine.connect()
@app.route("/requests")
def requests():
    t = ""
    for row in connection.execute("SELECT COUNT(*) FROM songs"):
        t = str(row[0]) + t
    return render_template('requestChoose.html', paginations=math.ceil((float(str(t))/25)))

@app.route("/getTable/<index>")
def getTable(index):
    index = MySQLdb.escape_string(index)
    t = connection.execute("SELECT * FROM songs ORDER BY `artist` LIMIT " + str((int(index) - 1) * 25) + ", 25")
    m = ""
    for x in t:
        m = m + "<tr>" + "<td>" + str(x["ID"]) + "</td>" + "<td>" + str(x["artist"]) + "</td>" + "<td>" + str(x["title"]) + "</td>" + '''<td><a href="reqForm/''' + str(x["ID"]) + '''"><button type="button">Request Song</button></a></td>''' + "</tr>"
    return '<table border="1" style="width:100%"><tr style="font-size: 30px;"><td>ID</td><td>Artist</td><td>Title</td><td>Action</td></tr><br>' + m + "</table>"

@app.route("/json/getTable/<index>")
def json_getTable(index):
    index = MySQLdb.escape_string(index)
    t = connection.execute("SELECT * FROM songs ORDER BY `artist` LIMIT " + str((int(index) - 1) * 25) + ", 25")
    m = ""
    for x in t:
        m = m + str(json.dumps({"ID": str(x["ID"]), "artist": str(x["artist"]), "title": str(x["title"])}))
    return m

@app.route("/json/tablePageCount")
def json_pagesCount():
    a = ""
    for row in connection.execute("SELECT COUNT(*) FROM songs"):
        a = str(row[0]) + a
    a = str(json.dumps({"pagesCount": math.ceil((float(str(a))/25))}))
    return a

@app.route("/searchTable/<query>")
def searchTable(query):
    query = MySQLdb.escape_string(query)
    t = connection.execute("SELECT * FROM songs WHERE `artist` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%' OR `title` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%'")
    m = ""
    for x in t:
        m = m + "<tr>" + "<td>" + str(x["ID"]) + "</td>" + "<td>" + str(x["artist"]) + "</td>" + "<td>" + str(x["title"]) + "</td>" + '''<td><a href="reqForm/''' + str(x["ID"]) + '''"><button type="button">Request Song</button></a></td>''' + "</tr>"
    return '<table border="1" style="width:100%"><tr style="font-size: 30px;"><td>ID</td><td>Artist</td><td>Title</td><td>Action</td></tr><br>' + m + "</table>"

@app.route("/json/searchTable/<query>")
def json_searchTable(query):
    query = MySQLdb.escape_string(query)
    t = connection.execute("SELECT * FROM songs WHERE `artist` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%' OR `title` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%'")
    m = ""
    for x in t:
        m = m + str(json.dumps({"ID": str(x["ID"]), "artist": str(x["artist"]), "title": str(x["title"])}))
    return m

@app.route("/reqForm/<songid>")
def requestForm(songid):
    songid = MySQLdb.escape_string(songid)
    t = connection.execute("SELECT * FROM songs WHERE `ID` LIKE  " + str(int(songid)))
    reqID = ""
    reqTITLE = ""
    reqARTIST = ""
    for x in t:
        reqID = str(x["ID"]) + reqID
        reqTITLE = strip_non_ascii(str(x["title"])) + reqTITLE
        reqARTIST = strip_non_ascii(str(x["artist"])) + reqARTIST
    return render_template('requestForm.html', reqID=reqID, reqTITLE=reqTITLE, reqARTIST=reqARTIST)

@app.route("/request-post", methods=['POST', 'GET'])
def request_post():
    if request.method == 'POST':
        trusted_proxies = {'127.0.0.1'}  # define your own set
        route = request.access_route + [request.remote_addr]
        remote_addr = next((addr for addr in reversed(route)
                            if addr not in trusted_proxies), request.remote_addr)

        reqSONGID = MySQLdb.escape_string(str(request.form['reqSONGID']))
        reqUSERNAME = MySQLdb.escape_string(str(request.form['reqUSERNAME'])).replace("%", "")
        reqIP = str(remote_addr)
        reqMSG = MySQLdb.escape_string(str(request.form['reqMSG'])).replace("%", "")
        reqTIMESTAMP = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        t = connection.execute("SELECT * FROM songs WHERE `ID` LIKE  " + str(int(reqSONGID)))
        reqID = ""
        reqTITLE = ""
        reqARTIST = ""
        for x in t:
            reqID = str(x["ID"]) + reqID
            reqTITLE = strip_non_ascii(str(x["title"])) + reqTITLE
            reqARTIST = strip_non_ascii(str(x["artist"])) + reqARTIST
        date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'))
        t = connection.execute('''SELECT COUNT(*) FROM requests WHERE `requested` LIKE "%%''' + date + '''%%" AND `userIP` LIKE "''' + reqIP + '''"''')
        m = ""
        for z in t:
            m = str(z[0]) + m
        if int(float(m)) >= 10:
            return render_template('requestErrorInQueue.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST, reqUSERNAME=reqUSERNAME, errorMESSAGE="you had reached the maximum daily limit (10) of requested songs. Give others a chance to shine too! Thank you for your understanding and check back tomorrow to beable to request more songs!")
        t = connection.execute("""SELECT * FROM queuelist WHERE `songID` LIKE """ + str(reqID))
        for x in t:
            if str(x["songID"]) == reqID:
                return render_template('requestErrorInQueue.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST, reqUSERNAME=reqUSERNAME, errorMESSAGE="the song you had requested is already in queue. Don't worry, as your song might be after within the next few songs.")
        connection.execute("""INSERT INTO `requests` (`songID`, `username`, `userIP`, `message`, `requested`) VALUES (""" + str(reqSONGID) + """, '""" + reqUSERNAME + """', '""" + reqIP + """', '""" + reqMSG + """', '""" + reqTIMESTAMP + """');""")
        return render_template('requestConfirmation.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST, reqUSERNAME=reqUSERNAME)
    return "GET IS NOT SUPPORTED ON /request-post", 403
#End Requests System

#For the bot
@app.route("/bot-request-post", methods=['POST'])
def bot_request_post():
    reqSONGID = MySQLdb.escape_string(str(request.form['reqSONGID']))
    reqUSERNAME = MySQLdb.escape_string(str(request.form['reqUSERNAME'])).replace("%", "")
    reqIP = "BOTREQUEST"
    reqMSG = ""
    reqTIMESTAMP = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'))
    t = connection.execute("""SELECT * FROM queuelist WHERE `songID` LIKE """ + str(reqSONGID))
    for x in t:
        if str(x["songID"]) == reqSONGID:
            return "The song you had requested is already in queue. Don't worry, as your song might be after within the next few songs."
    connection.execute("""INSERT INTO `requests` (`songID`, `username`, `userIP`, `message`, `requested`) VALUES (""" + str(reqSONGID) + """, '""" + reqUSERNAME + """', '""" + reqIP + """', '""" + reqMSG + """', '""" + reqTIMESTAMP + """');""")
    return "1"

@app.route("/json/bot-request-post", methods=['POST'])
def json_bot_request_post():
    reqSONGID = MySQLdb.escape_string(str(request.form['reqSONGID']))
    reqUSERNAME = MySQLdb.escape_string(str(request.form['reqUSERNAME'])).replace("%", "")
    reqIP = "BOTREQUEST"
    reqMSG = ""
    reqTIMESTAMP = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'))
    t = connection.execute("""SELECT * FROM queuelist WHERE `songID` LIKE """ + str(reqSONGID))
    for x in t:
        if str(x["songID"]) == reqSONGID:
            return str(json.dumps({"message": "The song you had requested is already in queue. Don't worry, as your song might be after within the next few songs.", "error": 1}))
    connection.execute("""INSERT INTO `requests` (`songID`, `username`, `userIP`, `message`, `requested`) VALUES (""" + str(reqSONGID) + """, '""" + reqUSERNAME + """', '""" + reqIP + """', '""" + reqMSG + """', '""" + reqTIMESTAMP + """');""")
    return str(json.dumps({"message": "Succesful request!", "error": 0}))

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
