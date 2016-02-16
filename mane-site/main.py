from flask import Flask, render_template
from xml2dict import ElementTree, XmlListConfig, XmlDictConfig
from crossdomainfuncs import crossdomain
import urllib2
import json
import commands

app = Flask(__name__)
gitRevision = commands.getoutput("git rev-parse --short master")

def getMFRTumblr():
    response = urllib2.urlopen('http://maneframeradio.tumblr.com/api/read?type=post&start=0&num=10')
    html = response.read()
    root = ElementTree.XML(html)
    xmldict = XmlDictConfig(root)
    xmldict = xmldict["posts"]
    x = xmldict["post"]
    return x


@app.route('/')
def index():
    t = getMFRTumblr()
    t = t[0]
    postTitle = t["regular-title"]
    postContent = t["regular-body"]
    postURL = t["url"]
    postTimestamp = t["date"]
    return render_template('header.html', title="Welcome") + render_template('menu.html', animatedMenubar="animated fadeInDown") + render_template('index.html', postTitle = postTitle, postContent = postContent, postURL = postURL, postTimestamp = postTimestamp) + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/about')
def about():
    return render_template('header.html', title="About") + render_template('menu.html', activeAbout="active") + render_template('about.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/blog')
def blog():
    t = getMFRTumblr()
    posts = []
    for x in t:
        a = {'title': x["regular-title"], 'url': x["url"], 'timestamp': x["date"], 'content': x["regular-body"]}
        posts.append(a)
    return render_template('header.html', title="Blog") + render_template('menu.html', activeBlog="active") + render_template('blog.html', posts=posts) + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/events')
def events():
    return render_template('header.html', title="Events") + render_template('menu.html', activeEvents="active") + render_template('events.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/team')
def team():
    return render_template('header.html', title="Team") + render_template('menu.html', activeTeam="active") + render_template('team.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/donate')
def donate():
    return render_template('header.html', title="Donate") + render_template('menu.html', activeDonate="active") + render_template('donate.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/contact')
def contact():
    return render_template('header.html', title="Contact") + render_template('menu.html', activeContact="active") + render_template('contact.html') + render_template('sidebar.html', revision=gitRevision) + render_template('player.html') + render_template('footer.html')

@app.route('/update_radio_subtxt', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def update_radio_subtxt():
    response = urllib2.urlopen('http://radio.mane-frame.com/status-json.xsl')
    xsl = response.read()
    mfr_json = json.loads(xsl)
    mfr_json = mfr_json["icestats"]["source"]
    mfr_json.pop()
    mfr_json = mfr_json.pop()
    return str(mfr_json["title"]) + " <em>" + str(mfr_json["listeners"]) + "</em>"

@app.route('/debug')
def debug():
    return commands.getoutput("git rev-parse --short master")

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')