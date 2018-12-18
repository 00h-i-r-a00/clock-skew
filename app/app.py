import os
from flask import Flask
from flask import render_template
from flask import request
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku``

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#indicate to the web application where the database will be stored
postgres_url = 'postgres://favlpjtwngyxmo:16331a96a43a27f46cd02cf9af66a89f9fa07594ddc5b2c2fbc168b2df38b05a@ec2-23-21-122-141.compute-1.       amazonaws.com:5432/d7vhvov24eqmvt'
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url
#initialize a connection to the database; use the db variable to interact with the database
db = SQLAlchemy()
db.init_app(app)
db.app = app
db.create_all()

##define a model for the user

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(1024), index=True)
    clock = db.Column(db.String(1024), index=True)

    def __repr__(self):
        return "<User-Agent: {}, Clock: {}".format(self.user_agent, self.clock)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        user_agent_received = request.headers.get('User-Agent')
        clock_received = request.get_json()
        user = User(user_agent=user_agent_received, clock=clock_received['time'])

        print (user)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()

    users = User.query.all()

    return render_template("home.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
