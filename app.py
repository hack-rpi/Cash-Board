from flask import Flask, jsonify, render_template, request
from flask.ext.login import LoginManager, UserMixin, login_required
import os
from pymongo import MongoClient
import json

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    #Init mongo database here
    

    def __init__(self, username, password):
        self.id = username
        self.password = password

    #Need to re-write to deal with mongo database
    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

#Play around with this
@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None

#TODO make Home page
#TODO make login form/page
#TODO make redirect
#TODO make collection for handling

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
    # Use g.user to get current user from flask-login
