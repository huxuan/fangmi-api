#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Message related API.
"""
from datetime import date

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

message = Blueprint('message', __name__)
api = Api(message)


def content_type(content):
    if isinstance(content, datastructures.FileStorage):
        return content
    else:
        return unicode(content)


class MessageAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        """ 获取单条信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/message?id=1
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "message_item": {
                    ...
                }
            }

        :<header Authorization: OAuth access_token，只有发件人和收件人才有权限
        :param id: **Required** 消息 ID
        :type id: int
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json object message_item: 消息的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args(request)
        message = models.Message.get(args['id'])
        message.verify_owner(request.oauth.user.username)
        payload = dict(
            message_item=message.serialize(),
        )
        return utils.api_response(payload=payload)


    @oauth.require_oauth()
    def post(self):
        """ 发送一条消息

        **Example Request**:

        .. sourcecode:: http

            POST /api/message
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="to_username"

            u2
            --AaB03x
            Content-Disposition: form-data; name="type"

            1
            --AaB03x
            Content-Disposition: form-data; name="content"

            message_content
            --AaB03x--

            POST /api/message
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="to_username"

            u2
            --AaB03x
            Content-Disposition: form-data; name="type"

            2
            --AaB03x
            Content-Disposition: form-data; name="content"
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of content ...
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "messages": [
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
        :form id: 收藏房屋的 ID
        :form type: 消息类型，1: 文本，2：图片
        :form content: 消息内容，文本消息对应文本内容，图片消息对应图片文件
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array messages: 消息列表的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('to_username', required=True)
        parser.add_argument('type', type=int, required=True)
        parser.add_argument('content', type=content_type,
            location=('files', 'json', 'values'))
        args = parser.parse_args(request)
        args['from_username'] = request.oauth.user.username
        message = models.Message.create(**args)
        payload = dict(
            messages=[message.serialize()],
        )
        return utils.api_response(payload=payload)


class ListAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @oauth.require_oauth()
    def get(self):
        """ 获取消息列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/message/list?from_username=u1&filter_unread=True
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "messages": [
                    {
                        ...
                    },
                    {
                        ...
                    },
                    ...
                ]
            }

        :<header Authorization: OAuth access_token，只有发件人和收件人才有权限
        :param from_username: **Required** 聊天对象用户名
        :type from_username: string
        :param filter_unread: 是否筛选未读条目，默认为 True
        :type filter_unread: boolean
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        :>json array messages: 消息列表的 serialize 信息
        """
        parser = self.parser.copy()
        parser.add_argument('from_username', required=True)
        parser.add_argument('filter_unread', type=inputs.boolean, default=True)
        args = parser.parse_args(request)
        args['to_username'] = request.oauth.user.username
        messages = models.Message.gets(**args)
        payload = dict(
            messages=[message.serialize() for message in messages],
        )
        return utils.api_response(payload=payload)


class ConversationAPI(Resource):

    @oauth.require_oauth()
    def get(self):
        """ 获取对话列表

        **Example Request**:

        .. sourcecode:: http

            GET /api/message/conversation
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "conversations": [
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
        :>json array conversations: 对话列表的 serialize 信息，\
每条为该对话的最新一条消息
        """
        payload = dict(
            conversations = request.oauth.user.get_conversion(),
        )
        return utils.api_response(payload=payload)

api.add_resource(MessageAPI, '')
api.add_resource(ListAPI, '/list')
api.add_resource(ConversationAPI, '/conversation')
