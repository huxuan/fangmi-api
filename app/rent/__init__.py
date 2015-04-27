#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Rent related API.
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

rent = Blueprint('rent', __name__)
api = Api(rent)


class RentAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        rent = models.Rent.get(args['id'])
        rent.verify_owner(request.oauth.user.username)
        payload = dict(
            rent=rent.serialize(),
        )
        return utils.api_response(payload=payload)


    @oauth.require_oauth()
    def post(self):
        parser = self.parser.copy()
        parser.add_argument('room_id', type=int, required=True)
        parser.add_argument('date_start', type=utils.strpdate, required=True)
        parser.add_argument('date_end', type=utils.strpdate, required=True)
        args = parser.parse_args(request)
        args['username'] = request.oauth.user.username
        rent = models.Rent.create(**args)
        payload = dict(
            rent=rent.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        parser = self.parser.copy()
        parser.add_argument('apartment_id', type=int)
        args = parser.parse_args(request)
        if args.get('apartment_id'):
            apartment = models.Apartment.get(args['apartment_id'])
            apartment.verify_owner(request.oauth.user.username)
        payload = dict(
            rents=[rent.serialize()
                for rent in models.Rent.gets(**args)],
        )
        return utils.api_response(payload=payload)

api.add_resource(RentAPI, '')
api.add_resource(ListAPI, '/list')
