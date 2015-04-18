#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: init file for app.
"""
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
api = Api(app)
oauth = OAuth2Provider(app)

from app.api import bp_api
from app.oauth import bp_oauth

app.register_blueprint(bp_oauth, url_prefix='/oauth')
app.register_blueprint(bp_api, url_prefix='/api')

from app import models

@app.route('/')
@app.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
