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
        payload = dict(
            conversations = request.oauth.user.get_conversion(),
        )
        return utils.api_response(payload=payload)

api.add_resource(MessageAPI, '')
api.add_resource(ListAPI, '/list')
api.add_resource(ConversationAPI, '/conversation')
