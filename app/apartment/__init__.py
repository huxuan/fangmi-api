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
from werkzeug import datastructures

from .. import models
from .. import utils
from ..oauth import oauth
from ..utils import reqparse

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
        # NOTE(huxuan): We may need validation for post data here.
        args = request.get_json()
        apartment = models.Apartment.create(
            address=args['address'],
            devices=args['devices'],
            num_bedroom=args['num_bedroom'],
            num_livingroom=args['num_livingroom'],
            reserve_choices=args['reserve_choices'],
            rooms=args['rooms'],
            subtitle=args['subtitle'],
            tags=args['tags'],
            title=args['title'],
            type=args['type'],
        )
        return utils.api_response(payload=apartment.serialize())


class ApartmentPhotosAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, required=True)
        self.parser.add_argument('contract',
            type=datastructures.FileStorage,
            location='files',
        )
        self.parser.add_argument('photos',
            type=datastructures.FileStorage,
            location='files',
            action='append',
        )

    @oauth.require_oauth()
    def post(self):
        print request.files
        args = self.parser.parse_args(request)
        print args['photos']
        apartment = models.Apartment.get(args['id'])
        user = request.oauth.user
        if apartment.verify_owner(user.username):
            apartment.set(**args)
        return utils.api_response(payload=apartment.serialize())


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
api.add_resource(ApartmentPhotosAPI, '/photos')
api.add_resource(ApartmentListAPI, '/list')
