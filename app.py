from flask import Flask, jsonify, render_template, request, redirect, abort
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user

import os
import ConfigParser
from pymongo import MongoClient
import json
import util/mongoCalls as MC

config = ConfigParser.ConfigParser()
config.read('dbConfig.cfg')
mogoUri =  config.get('Development', 'url')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#database Login
maxSevSelDelay = 1
client = MongoClient(mogoUri, serverSelectionTimeoutMS=maxSevSelDelay)


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# some protected url
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cool')
@login_required
def home():
    return Response("Hello World!")

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        valid, data = MC.checkUser()
        if valid:
            id = data['_id']
            user = User(id)
            login_user(user)
            return {message: 'User Known', userInfo: data}, 200
        else:
            return abort(401)
    else:
        return render_template('login.html')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    app.run()
