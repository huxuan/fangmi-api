#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: ReserveChoice related API.
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

reserve_choice = Blueprint('reserve_choice', __name__)
api = Api(reserve_choice)


class ReserveChoiceAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        reserve_choice = models.ReserveChoice.get(args['id'])
        payload = dict(
            reserve_choice=reserve_choice.serialize(),
        )
        return utils.api_response(payload=payload)


    @oauth.require_oauth()
    def post(self):
        parser = self.parser.copy()
        parser.add_argument('apartment_id', type=int, required=True)
        parser.add_argument('date', type=utils.strpdate, required=True)
        parser.add_argument('time_start', type=utils.strptime, required=True)
        parser.add_argument('time_end', type=utils.strptime, required=True)
        args = parser.parse_args(request)
        apartment = models.Apartment.get(args['apartment_id'])
        apartment.verify_owner(request.oauth.user.username)
        reserve_choice = models.ReserveChoice.create(**args)
        payload = dict(
            reserve_choice=reserve_choice.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        parser = self.parser.copy()
        parser.add_argument('apartment_id', type=int, required=True)
        args = parser.parse_args(request)
        apartment = models.Apartment.get(args['apartment_id'])
        payload = dict(
            reserve_choices=[reserve_choice.serialize()
                for reserve_choice in models.ReserveChoice.gets(**args)],
        )
        return utils.api_response(payload=payload)

api.add_resource(ReserveChoiceAPI, '')
api.add_resource(ListAPI, '/list')
