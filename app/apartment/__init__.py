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


def device_type(device, name):
    utils.parser_required(name, device, ['name', 'count'])
    device = utils.parser_parse(name, device, [('count', int)])
    return device


def reserve_choice_type(reserve_choice, name):
    utils.parser_required(name, reserve_choice,
        ['date', 'time_start', 'time_end'])
    reserve_choice = utils.parser_parse(name, reserve_choice,
        [
            ('date', utils.strpdate),
            ('time_start', utils.strptime),
            ('time_end', utils.strptime),
        ])
    return reserve_choice


def room_type(room, name):
    utils.parser_required(name, room,
        ['name', 'area', 'price', 'date_entrance'])
    room = utils.parser_parse(name, room,
        [('area', int), ('price', int), ('date_entrance', utils.strpdate)])
    return room


def tag_type(tag, name):
    utils.parser_required(name, tag, ['name'])
    return tag


class ApartmentAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, default=None)
        self.parser.add_argument('community_id', type=int)
        self.parser.add_argument('title')
        self.parser.add_argument('subtitle')
        self.parser.add_argument('address')
        self.parser.add_argument('num_bedroom', type=int)
        self.parser.add_argument('num_livingroom', type=int)
        self.parser.add_argument('type', type=int)
        self.parser.add_argument('devices', type=device_type, action='append')
        self.parser.add_argument('reserve_choices', type=reserve_choice_type,
            action='append')
        self.parser.add_argument('rooms', type=room_type, action='append')
        self.parser.add_argument('tags', type=tag_type, action='append')

    def get(self):
        args = self.parser.parse_args(request)
        apartment = models.Apartment.get(args['id'])
        payload = dict(
            apartment=apartment.serialize(),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
        user = request.oauth.user
        args = self.parser.parse_args(request)
        args['username'] = user.username
        apartment = models.Apartment.create(**args)
        payload = dict(
            apartment=apartment.serialize(),
        )
        return utils.api_response(payload=payload)


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
        args = self.parser.parse_args(request)
        apartment = models.Apartment.get(args['id'])
        user = request.oauth.user
        if apartment.verify_owner(user.username):
            apartment.set(**args)
        payload = dict(
            apartment=apartment.serialize(),
        )
        return utils.api_response(payload=payload)


class ApartmentListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username')
        self.parser.add_argument('community_id', type=int)

    def get(self):
        args = self.parser.parse_args(request)
        payload = dict(
            apartments=[apartment.serialize()
                for apartment in models.Apartment.gets(**args)],
        )
        return utils.api_response(payload=payload)


api.add_resource(ApartmentAPI, '')
api.add_resource(ApartmentPhotosAPI, '/photos')
api.add_resource(ApartmentListAPI, '/list')
