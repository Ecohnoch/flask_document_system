# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : app.py
# @Function : TODO
import os
import flask
import logging
from datetime import timedelta

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

import configs

def create_app():
    app = Flask(__name__)
    app.secret_key           = configs.app_secret_key
    app.config['MONGO_URI']  = configs.app_mongo_uri

    mongo = PyMongo(app=app)
    login_manager = LoginManager(app=app)
    return app, mongo, login_manager

app, mongo, login_manager = create_app()

