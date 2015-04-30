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
        payload = dict(
            schools=[school.serialize()
                for school in models.School.gets()],
        )
        return utils.api_response(payload=payload)


class SearchAPI(Resource):
    def get(self):
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
