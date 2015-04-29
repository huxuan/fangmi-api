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

    @oauth.require_oauth()
    def get(self):
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        apartment = models.Apartment.get(**args)
        payload = dict(
            apartment=apartment.serialize(oauth_user=request.oauth.user),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def put(self):
        parser = self.parser.copy()
        parser.add_argument('id', type=int)
        parser.add_argument('title')
        parser.add_argument('subtitle')
        parser.add_argument('address')
        parser.add_argument('num_bedroom', type=int)
        parser.add_argument('num_livingroom', type=int)
        parser.add_argument('type', type=int)
        parser.add_argument('devices', type=device_type, action='append')
        parser.add_argument('reserve_choices', type=reserve_choice_type,
            action='append')
        parser.add_argument('rooms', type=room_type, action='append')
        parser.add_argument('tags', type=tag_type, action='append')
        args = parser.parse_args(request)
        apartment = models.Apartment.get(args['id'])
        apartment.verify_owner(request.oauth.user.username)
        apartment.set(**args)
        payload = dict(
            apartment=apartment.serialize(),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
        parser = self.parser.copy()
        parser.add_argument('community_id', type=int, required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('subtitle', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('num_bedroom', type=int, required=True)
        parser.add_argument('num_livingroom', type=int, required=True)
        parser.add_argument('type', type=int)
        parser.add_argument('devices', type=device_type, action='append',
            required=True)
        parser.add_argument('reserve_choices', type=reserve_choice_type,
            action='append', required=True)
        parser.add_argument('rooms', type=room_type, action='append',
            required=True)
        parser.add_argument('tags', type=tag_type, action='append')
        args = parser.parse_args(request)
        args['username'] = request.oauth.user.username
        apartment = models.Apartment.create(**args)
        payload = dict(
            apartment=apartment.serialize(),
        )
        return utils.api_response(payload=payload)


class PhotosAPI(Resource):
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


class FavoriteAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', required=True)
        self.parser.add_argument('action', default='append',
            choices=('append', 'remove'))

    @oauth.require_oauth()
    def get(self):
        user = request.oauth.user
        payload = dict(
            apartments=user.fav_apartments,
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
        args = self.parser.parse_args(request)
        user = request.oauth.user
        user.fav_apartment_action(args['id'], args['action'])
        payload = dict(
            apartments=user.fav_apartments,
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username')
        self.parser.add_argument('community_id', type=int)
        self.parser.add_argument('school_id', type=int)

    def get(self):
        args = self.parser.parse_args(request)
        payload = dict(
            apartments=[apartment.serialize()
                for apartment in models.Apartment.gets(**args)],
        )
        return utils.api_response(payload=payload)


class SearchAPI(Resource):
    @oauth.require_oauth()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', required=True)
        args = parser.parse_args(request)
        payload = dict(
            apartments=[apartment.serialize()
                for apartment in models.Apartment.search(**args)],
        )
        return utils.api_response(payload=payload)


api.add_resource(ApartmentAPI, '')
api.add_resource(PhotosAPI, '/photos')
api.add_resource(FavoriteAPI, '/fav')
api.add_resource(ListAPI, '/list')
api.add_resource(SearchAPI, '/search')
