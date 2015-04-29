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
        payload = dict(
            communities=[community.serialize()
                for community in models.Community.gets()],
        )
        return utils.api_response(payload=payload)


class SearchAPI(Resource):
    @oauth.require_oauth()
    def get(self):
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
