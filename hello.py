#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.debug = True
    app.host = '0.0.0.0'
    app.run()