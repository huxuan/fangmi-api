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
from ..utils import reqparse

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


class UserListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', action='append', default=[])

    def get(self):
        args = self.parser.parse_args(request)
        payload = dict(
            users=[models.User.get(username).serialize()
                for username in args['username']]
        )
        return utils.api_response(payload=payload)


api.add_resource(UserAPI, '')
api.add_resource(UserListAPI, '/list')
