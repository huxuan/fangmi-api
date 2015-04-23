#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Apartment Related API.
"""
from flask import Blueprint
from flask import request
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from .. import models
from .. import utils
from ..oauth import oauth

apartment = Blueprint('apartment', __name__)
api = Api(apartment)


class ApartmentAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, default=None)

    def get(self):
        args = self.parser.parse_args(request)
        apartment = models.Apartment.get(args['id'])
        return utils.api_response(payload=apartment.serialize())

    @oauth.require_oauth()
    def post(self):
        apartment = models.Apartment.create(
            address=request.json['address'],
            devices=request.json['devices'],
            num_bedroom=request.json['num_bedroom'],
            num_livingroom=request.json['num_livingroom'],
            reserve_choices=request.json['reserve_choices'],
            rooms=request.json['rooms'],
            subtitle=request.json['subtitle'],
            tags=request.json['tags'],
            title=request.json['title'],
        )


class ApartmentListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', action='append', default=[])

    def get(self):
        args = self.parser.parse_args(request)
        payload = dict(
            apartments=[models.Apartment.get(id).serialize()
                for id in args['id']]
        )
        return utils.api_response(payload=payload)


api.add_resource(ApartmentAPI, '')
api.add_resource(ApartmentListAPI, '/list')
