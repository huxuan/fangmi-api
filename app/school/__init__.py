#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: School related API.
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

school = Blueprint('school', __name__)
api = Api(school)


class SchoolAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        """ 获取学校信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/school?id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "school": {
                    ...
                }
            }

        :param int id: **Required** 学校 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object school: 学校的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        school = models.School.get(args['id'])
        payload = dict(
            school=school.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def get(self):
        """ 获取学校列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/school/list

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "schools": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array schools: 学校列表的 serialize 信息
        """
        payload = dict(
            schools=[school.serialize()
                for school in models.School.gets()],
        )
        return utils.api_response(payload=payload)


class SearchAPI(Resource):
    def get(self):
        """ 搜索学校

        **Example Request**:

        .. sourcecode:: http

            GET /api/school/search?q=test

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "schools": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :param string q: **Required** 检索关键词
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array schools: 学校列表的 serialize 信息
        """
        parser = reqparse.RequestParser()
        parser.add_argument('q', required=True)
        args = parser.parse_args(request)
        payload = dict(
            schools=[school.serialize()
                for school in models.School.search(**args)],
        )
        return utils.api_response(payload=payload)


api.add_resource(SchoolAPI, '')
api.add_resource(ListAPI, '/list')
api.add_resource(SearchAPI, '/search')
