from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.paginate import Pagination
from sqlalchemy import *
import json
import os
import MySQLdb
import time
import datetime
import math
app = Flask(__name__)

def file_get_contents(filename):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename) as f:
        return f.read()

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

@app.route("/searchTable/<query>")
def searchTable(query):
    query = MySQLdb.escape_string(query)
    t = connection.execute("SELECT * FROM songs WHERE `artist` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%' OR `title` COLLATE UTF8_GENERAL_CI LIKE '%%" + str(query) + "%%'")
    m = ""
    for x in t:
        m = m + "<tr>" + "<td>" + str(x["ID"]) + "</td>" + "<td>" + str(x["artist"]) + "</td>" + "<td>" + str(x["title"]) + "</td>" + '''<td><a href="reqForm/''' + str(x["ID"]) + '''"><button type="button">Request Song</button></a></td>''' + "</tr>"
    return '<table border="1" style="width:100%"><tr style="font-size: 30px;"><td>ID</td><td>Artist</td><td>Title</td><td>Action</td></tr><br>' + m + "</table>"

@app.route("/reqForm/<songid>")
def requestForm(songid):
    songid = MySQLdb.escape_string(songid)
    t = connection.execute("SELECT * FROM songs LIMIT 1 OFFSET " + str(int(songid) - 1))
    reqID = ""
    reqTITLE = ""
    reqARTIST = ""
    for x in t:
        reqID = str(x["ID"]) + reqID
        reqTITLE = str(x["title"]) + reqTITLE
        reqARTIST = str(x["artist"]) + reqARTIST
    return render_template('requestForm.html', reqID=reqID, reqTITLE=reqTITLE, reqARTIST=reqARTIST)

@app.route("/request-post", methods=['POST', 'GET'])
def request_post():
    if request.method == 'POST':
        trusted_proxies = {'127.0.0.1'}  # define your own set
        route = request.access_route + [request.remote_addr]
        remote_addr = next((addr for addr in reversed(route)
                            if addr not in trusted_proxies), request.remote_addr)

        reqSONGID = MySQLdb.escape_string(str(request.form['reqSONGID']))
        reqUSERNAME = MySQLdb.escape_string(str(request.form['reqUSERNAME']))
        reqIP = str(remote_addr)
        reqMSG = MySQLdb.escape_string(str(request.form['reqMSG']))
        reqTIMESTAMP = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        t = connection.execute("SELECT * FROM songs LIMIT 1 OFFSET " + str(int(reqSONGID) - 1))
        reqID = ""
        reqTITLE = ""
        reqARTIST = ""
        for x in t:
            reqID = str(x["ID"]) + reqID
            reqTITLE = str(x["title"]) + reqTITLE
            reqARTIST = str(x["artist"]) + reqARTIST
        connection.execute("""INSERT INTO `requests` (`songID`, `username`, `userIP`, `message`, `requested`) VALUES (""" + str(reqSONGID) + """, '""" + reqUSERNAME + """', '""" + reqIP + """', '""" + reqMSG + """', '""" + reqTIMESTAMP + """');""")
        return render_template('requestConfirmation.html', reqID=reqSONGID, reqTITLE=reqTITLE, reqARTIST=reqARTIST, reqUSERNAME=reqUSERNAME)
    return "GET IS NOT SUPPORTED ON /request-post"

if __name__ == "__main__":
    app.debug = True
    app.run(host= '0.0.0.0')
