#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: init file for app.
"""
from functools import partial

from flask import Flask
from flask import jsonify
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

cors = CORS(app)
db = SQLAlchemy(app)

from app import models
from app import utils

from app.account import account
from app.apartment import apartment
from app.api import bp_api
from app.oauth import bp_oauth
from app.rent import rent
from app.uploads import uploads
from app.user import user

app.register_blueprint(account, url_prefix='/api/account')
app.register_blueprint(apartment, url_prefix='/api/apartment')
app.register_blueprint(bp_api, url_prefix='/api')
app.register_blueprint(bp_oauth, url_prefix='/oauth')
app.register_blueprint(rent, url_prefix='/api/rent')
app.register_blueprint(uploads, url_prefix='/uploads')
app.register_blueprint(user, url_prefix='/api/user')

# NOTE(huxuan): Use Flask's error handler instead of the one in flask-restful.
app.handle_exception = partial(Flask.handle_exception, app)
app.handle_user_exception = partial(Flask.handle_user_exception, app)

@app.errorhandler(utils.APIException)
def error_handler(api_exception):
    return jsonify(api_exception.to_dict())

@app.route('/')
@app.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
