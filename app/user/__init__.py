#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: User related API.
"""
from flask import Blueprint
from flask import request
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from .. import models
from .. import utils
from ..oauth import oauth

user = Blueprint('user', __name__)
api = Api(user)


class UserAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)

    def get(self):
        args = self.parser.parse_args(request)
        user = models.User.get(args['username'])
        return utils.api_response(payload=user.serialize())


api.add_resource(UserAPI, '')
