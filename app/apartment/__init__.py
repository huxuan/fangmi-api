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
from flask.ext.restful import inputs
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
        """ 获取房屋信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/apartment?id=1
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartment": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :query int id: **Required** 房屋 ID
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object apartment: 房屋的 serialize 信息
        """
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
        """ 更新房屋信息

        **Example Request**:

        .. sourcecode:: http

            PUT /api/apartment
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: application/json

            {
                "id": 1,
                "community_id": 1,
                "title": "title1",
                "subtitle": "subtitle1",
                "address": "address1",
                "num_bedroom": 3,
                "num_livingroom": 1,
                "type": 0,
                "devices": [
                    {"name": "name1", "count": 1},
                    {"name": "name2", "count": 3}
                ], "reserve_choices": [
                    {"date": "1950-10-01", "time_start": "12:34:56",
                        "time_end": "12:56:34"},
                    {"date": "1951-10-01", "time_start": "12:34:56",
                        "time_end": "12:56:34"}
                ], "rooms": [
                    {"name": "主卧", "area": 88, "price": 8888,
                        "date_entrance": "1949-10-01"},
                    {"name": "次卧1", "area": 66, "price": 6666,
                        "date_entrance": "1950-10-01"}
                ], "tags": [
                    {"name": "标签1"},
                    {"name": "标签2"},
                    {"name": "标签3"}
                ]
            }

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartment": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :<json int id: **Required**, 房屋 ID
        :<json int community_id: 小区 ID
        :<json string title: 标题
        :<json string subtitle: 副标题
        :<json string address: 地址
        :<json int num_bedroom: 卧室个数
        :<json int num_livingroom: 客厅个数
        :<json int type: 房屋类型，0: 整租，1: 合租
        :<json array devices: 房屋设备
        :<json array reserve_choices: 预约时间
        :<json array rooms: 房屋信息，整租的话就只用一个 room 来存面积等信息
        :<json array tags: 标签
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object apartment: 房屋的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('community_id', type=int)
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
        parser.add_argument('cancelled', type=inputs.boolean)
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
        """ 新建房屋信息

        **Example Request**:

        .. sourcecode:: http

            PUT /api/apartment
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: application/json

            {
                "community_id": 1,
                "title": "title1",
                "subtitle": "subtitle1",
                "address": "address1",
                "num_bedroom": 3,
                "num_livingroom": 1,
                "type": 0,
                "devices": [
                    {"name": "name1", "count": 1},
                    {"name": "name2", "count": 3}
                ], "reserve_choices": [
                    {"date": "1950-10-01", "time_start": "12:34:56",
                        "time_end": "12:56:34"},
                    {"date": "1951-10-01", "time_start": "12:34:56",
                        "time_end": "12:56:34"}
                ], "rooms": [
                    {"name": "主卧", "area": 88, "price": 8888,
                        "date_entrance": "1949-10-01"},
                    {"name": "次卧1", "area": 66, "price": 6666,
                        "date_entrance": "1950-10-01"}
                ], "tags": [
                    {"name": "标签1"},
                    {"name": "标签2"},
                    {"name": "标签3"}
                ]
            }

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartment": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :<json int community_id: **Required**, 小区 ID
        :<json string title: **Required**, 标题
        :<json string subtitle: **Required**, 副标题
        :<json string address: **Required**, 地址
        :<json int num_bedroom: **Required**, 卧室个数
        :<json int num_livingroom: **Required**, 客厅个数
        :<json int type: **Required**, 房屋类型，0: 整租，1:合租
        :<json array devices: **Required**, 房屋设备
        :<json array reserve_choices: **Required**, 预约时间
        :<json array rooms: **Required**, 房屋信息，整租的话就只用一个 room 来存面积等信息
        :<json array tags: **Required**, 标签
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object apartment: 房屋的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('community_id', type=int, required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('subtitle', required=True)
        parser.add_argument('address', required=True)
        parser.add_argument('num_bedroom', type=int, required=True)
        parser.add_argument('num_livingroom', type=int, required=True)
        parser.add_argument('type', type=int, default=0)
        parser.add_argument('devices', type=device_type, action='append',
            default=[])
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
        """ 提交房屋图片信息

        **Example Request**:

        .. sourcecode:: http

            POST /api/apartment/photos
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="id"

            1
            --AaB03x
            Content-Disposition: form-data; name="contract";
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of contract ...
            --AaB03x
            Content-Disposition: form-data; name="photos";
            Content-Type: multipart/mixed; boundary=BbC04y

            --BbC04y
            Content-Disposition: file;
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of photo1 ...
            --BbC04y
            Content-Disposition: file;
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of photo2 ...
            --BbC04y
            ...
            --BbC04y--
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartment": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token
        :<json int id: **Required**, 房屋 ID
        :<json file contract: 合同文件
        :<json files photo: 房屋照片
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object apartment: 房屋的 serialize 信息
        """
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
        """ 获取用户收藏的房屋

        **Example Request**:

        .. sourcecode:: http

            GET /api/apartment/fav
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartments": [
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
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array apartments: 收藏房屋列表的 serialize 信息
        """
        user = request.oauth.user
        payload = dict(
            apartments=user.fav_apartments,
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
        """ 添加或删除用户收藏的房屋

        **Example Request**:

        .. sourcecode:: http

            POST /api/apartment/fav
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            id=1&action=append

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartments": [
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
        :query int id: 收藏房屋的 ID
        :query string action: ``append`` （添加） 或者 ``remove`` （删除）
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array apartments: 收藏房屋列表的 serialize 信息
        """
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
        self.parser.add_argument('q')
        self.parser.add_argument('filter_cancelled', type=inputs.boolean,
            default=True)
        self.parser.add_argument('filter_deleted', type=inputs.boolean,
            default=True)
        self.parser.add_argument('limit', type=int)

    @oauth.require_oauth()
    def get(self):
        """ 获取房屋列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/apartment/list?username=u1&community_id=1&school_id=2&\
q=test&filter_cancelled=true&filter_deleted=false&limit=10
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "apartments": [
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
        :query string username: 用户名，用于筛选房东
        :query int community_id: 小区 ID，用于筛选某一小区的房子
        :query int school_id: 学校 ID，用于筛选某一学校附近的房子
        :query string q: 检索关键词，用于搜索
        :query boolean filter_cancelled: 是否筛掉已经取消发布的房屋，默认为 True
        :query boolean filter_deleted: 是否筛掉已经标记为删除的房屋，默认为 True
        :query int limit: 返回结果数目上限
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array apartments: 房屋列表的 serialize 信息
        """
        args = self.parser.parse_args(request)
        payload = dict(
            apartments=[apartment.serialize()
                for apartment in models.Apartment.gets(**args)],
        )
        return utils.api_response(payload=payload)


api.add_resource(ApartmentAPI, '')
api.add_resource(PhotosAPI, '/photos')
api.add_resource(FavoriteAPI, '/fav')
api.add_resource(ListAPI, '/list')
