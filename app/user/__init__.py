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
        """ 获取用户信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/user?username=u1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                    ...
                }
            }

        :param string username: **Required** 用户名
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object user: 用户的 serialize 信息
        """
        args = self.parser.parse_args(request)
        user = models.User.get(args['username'])
        payload = dict(
            user=user.serialize()
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', action='append', default=[])

    def get(self):
        """ 获取用户列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/user/list?username=u1&username=u2&username=u3

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "users": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :param string username: 用户名（列表）
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array users: 用户列表的 serialize 信息
        """
        args = self.parser.parse_args(request)
        if args['username']:
            users = [models.User.get(username).serialize()
                for username in args['username']]
        else:
            users = [user.serialize()
                for user in models.User.gets()]
        payload = dict(
            users=users,
        )
        return utils.api_response(payload=payload)


api.add_resource(UserAPI, '')
api.add_resource(ListAPI, '/list')
