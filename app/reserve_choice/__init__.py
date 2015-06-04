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
        """ 获取预约选项信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/reserve_choice?id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve_choice": {
                    ...
                }
            }

        :param int id: **Required** 预约选项 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object reserve_choice: 预约选项的 serialize 信息
        """
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
        """ 新建预约选项

        **Example Request**:

        .. sourcecode:: http

            POST /api/reserve_choice
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            apartment_id=1&date=2015-05-01&time_start=12:34:56&time_end=12:56:34

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve_choice": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token, 只有房东才有权限
        :query int apartment_id: **Required** 房屋 ID
        :query date date: **Required** 预约日期
        :query time time_start: **Required** 预约开始时间
        :query time time_end: **Required** 预约结束时间
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object reserve_choice: 预约选项的 serialize 信息
        """
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
        """ 获取预约选项列表信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/reserve_choice/list?apartment_id=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "reserve_choices": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :param int apartment_id: 房屋 ID，用于筛选某一房屋的所有预约选项
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array reserve_choices: 预约选项列表的 serialize 信息
        """
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
