#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/<username>')
def show_user_profile(username):
    return "Hello " + username + "!"

if __name__ == "__main__":
    app.debug = True
    app.host = '0.0.0.0'
    app.run()