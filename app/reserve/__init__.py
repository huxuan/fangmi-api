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
        """ 获取预约记录信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/reserve
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token, 只有房东和房客才有权限
        :query int id: **Required** 预约记录 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object reserve: 预约记录的 serialize 信息
        """
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
        """ 新建预约记录

        **Example Request**:

        .. sourcecode:: http

            POST /api/reserve
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            reserve_choice_id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token, 只有房客才能调用，为自己新建
        :query int reserve_choice_id: **Required** 预约选项 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object reserve: 预约记录的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('reserve_choice_id', type=int, required=True)
        args = parser.parse_args(request)
        args['username'] = request.oauth.user.username
        reserve = models.Reserve.create(**args)
        payload = dict(
            reserve=reserve.serialize(),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def put(self):
        """ 修改预约记录

        **Example Request**:

        .. sourcecode:: http

            PUT /api/reserve
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            id=1&cancelled=true

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token, 只有房东和房客才有权限
        :query int id: **Required** 预约记录 ID
        :query boolean cancelled: **Required** 是否取消预约
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object reserve: 预约记录的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('cancelled', type=inputs.boolean, default=False)
        args = parser.parse_args(request)
        reserve = models.Reserve.get(args['id'])
        reserve.verify_owner(request.oauth.user.username)
        reserve.set(**args)
        payload = dict(
            reserve=reserve.serialize(),
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        """ 获取预约记录列表信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/reserve/list
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            username=u1&apartment_id=1&reserve_choice_id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserves": [
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
        :query string username: 用户名，用于筛选某用户的预约记录，\
只能是已登录用户自己的用户名
        :query int apartment_id: 房屋 ID，用于筛选某一房屋的所有预约记录，\
只有房东和已预约的房客才有权限
        :query int reserve_choice_id: 预约记录 ID，用于筛选同一预约选项的预约，\
只有房东和已预约的房客才有权限
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array reserves: 预约记录列表的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('username')
        parser.add_argument('apartment_id', type=int)
        parser.add_argument('reserve_choice_id', type=int)
        args = parser.parse_args(request)
        reserves = models.Reserve.gets(**args)
        models.Reserve.is_accessible(reserves, request.oauth.user.username)
        payload = dict(
            reserves=[reserve.serialize() for reserve in reserves],
        )
        return utils.api_response(payload=payload)

api.add_resource(ReserveAPI, '')
api.add_resource(ListAPI, '/list')
