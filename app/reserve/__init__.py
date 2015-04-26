#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Reserve related API.
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

reserve = Blueprint('reserve', __name__)
api = Api(reserve)


class ReserveAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        reserve = models.Reserve.get(args['id'])
        reserve.verify_owner(request.oauth.user.username)
        payload = dict(
            reserve=reserve.serialize(),
        )
        return utils.api_response(payload=payload)


    @oauth.require_oauth()
    def post(self):
        parser = self.parser.copy()
        parser.add_argument('reserve_choice_id', type=int, required=True)
        args = parser.parse_args(request)
        args['username'] = request.oauth.user.username
        reserve = models.Reserve.create(**args)
        payload = dict(
            reserve=reserve.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        parser = self.parser.copy()
        parser.add_argument('username')
        parser.add_argument('apartment_id', type=int)
        args = parser.parse_args(request)
        reserves = models.Reserve.gets(**args)
        for reserve in reserves:
            reserve.verify_owner(request.oauth.user.username)
        payload = dict(
            reserves=[reserve.serialize() for reserve in reserves],
        )
        return utils.api_response(payload=payload)

api.add_resource(ReserveAPI, '')
api.add_resource(ListAPI, '/list')
