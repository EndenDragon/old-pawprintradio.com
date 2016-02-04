from flask import Flask, request, redirect
from flask import session
import requests
import urllib2, urllib

app = Flask(__name__)

@app.route("/")
def hello():
    return """<a href="/login">Login to Poniverse</a>"""

@app.route("/login")
def login():
    return redirect("https://poniverse.net/oauth/authorize?response_type=code&client_id=wr8AtU523OrPBxvGAUWUjDrcRKbcidCoden1N1mR&redirect_uri=http://127.0.0.1:5000/login_process&state=EndenDragonFTW", code=302)
    
@app.route("/login_process")
def login_process():
    error = request.args.get("error")
    error_description = request.args.get("error_description")
    state = request.args.get("state")
    code = request.args.get("code")
    if error is None:
        if state != "EndenDragonFTW":
            return "state is invalid"
        else:
            URLaccess_token = "https://poniverse.net/oauth/access_token"
            values = requests.post("https://poniverse.net/oauth/access_token", data={"grant_type":"authorization_code","code":code,"redirect_uri":"http://127.0.0.1:5000","client_id":"wr8AtU523OrPBxvGAUWUjDrcRKbcidCoden1N1mR","client_secret":"6KWUrPjr96Z7UUxtwapKUunYRrW9KE4tF7fXk4u3"})
            return values
    else:
        return error + ": " + error_description


if __name__ == "__main__":
    app.debug = "True"
    app.run()