import os
from flask import Flask
from flask import render_template
from flask import request
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku``

project_dir = os.path.dirname(os.path.abspath(__file__))

#path to the database

#database_file = "postgresql:///{}".format(os.path.join(project_dir, "userdatabase.db"))

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#indicate to the web application where the database will be stored
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://xgtlvkylcqrehr:0ad1ba2bcc1e37c8cab6cf9d43d0023da75e5179c5feac328eb1eb0542b3a114@ec2-23-21-122-141.compute-1.amazonaws.com:5432/df6h3749rfbgev'
#initialize a connection to the database; use the db variable to interact with the databse
db = SQLAlchemy(app)
heroku = Heroku(app)

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
