#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Community related API.
"""
from datetime import date

from flask import Blueprint
from flask import request
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import inputs
from flask.ext.restful import reqparse

from .. import models
from .. import utils
from ..oauth import oauth
from ..utils import reqparse

community = Blueprint('community', __name__)
api = Api(community)


class CommunityAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        """ 获取小区信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/community?id=1
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "community": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :query int id: **Required** 小区 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object apartment: 小区的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        community = models.Community.get(args['id'])
        payload = dict(
            community=community.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    @oauth.require_oauth()
    def get(self):
        """ 获取小区列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/community/list
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "communities": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :<header Authorization: OAuth access_token
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array apartments: 小区列表的 serialize 信息
        """
        payload = dict(
            communities=[community.serialize()
                for community in models.Community.gets()],
        )
        return utils.api_response(payload=payload)


class SearchAPI(Resource):
    @oauth.require_oauth()
    def get(self):
        """ 搜索小区列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/community/search?q=test
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "communities": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :<header Authorization: OAuth access_token
        :query string q: **Required** 检索关键词
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array apartments: 小区列表的 serialize 信息
        """
        parser = reqparse.RequestParser()
        parser.add_argument('q', required=True)
        args = parser.parse_args(request)
        payload = dict(
            communities=[community.serialize()
                for community in models.Community.search(**args)],
        )
        return utils.api_response(payload=payload)


api.add_resource(CommunityAPI, '')
api.add_resource(ListAPI, '/list')
api.add_resource(SearchAPI, '/search')
