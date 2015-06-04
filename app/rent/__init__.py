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
        """ 获取租房记录信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/rent
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "rent": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :query int id: **Required** 租房记录 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object rent: 租房记录的 serialize 信息
        """
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
        """ 新建租房记录

        **Example Request**:

        .. sourcecode:: http

            POST /api/rent
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            room_id=1&date_start=2015-05-01&date_end=2016-05-01

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "rent": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :query int romm_id: **Required** 租房对应的房间 ID（注意是Room的，\
不是Apartment的）
        :query date date_start: **Required** 租房开始时间
        :query date date_end: **Required** 租房结束时间
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object rent: 租房记录的 serialize 信息
        """
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
        """ 获取租房记录列表信息

        如果不传 ``apartment_id`` 获得的是已登录用户自己的租房记录列表，
        如果传的话获得的是某间房屋的租房记录列表（只有房东才有权限）

        **Example Request**:

        .. sourcecode:: http

            GET /api/rent/list
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

            GET /api/rent/list
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            apartment_id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "rents": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :<header Authorization: OAuth access_token
        :query int apartment_id: 房屋 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array rents: 租房记录列表的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('apartment_id', type=int)
        args = parser.parse_args(request)
        if args.get('apartment_id'):
            apartment = models.Apartment.get(args['apartment_id'])
            apartment.verify_owner(request.oauth.user.username)
        else:
            args['username'] = request.oauth.user.username
        payload = dict(
            rents=[rent.serialize()
                for rent in models.Rent.gets(**args)],
        )
        return utils.api_response(payload=payload)

api.add_resource(RentAPI, '')
api.add_resource(ListAPI, '/list')
