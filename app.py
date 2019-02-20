import ssl
import os
from flask import Flask
from flask import render_template
from flask import request
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('time.securepki.org.crt', 'time.securepki.org.key')
app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, ssl_context=context, host='127.0.0.1', port='443')

