#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for api blueprint.
"""
from functools import partial

from flask import Blueprint
from flask import Flask
from flask import jsonify

from .. import models
import code

bp_api = Blueprint('api', __name__)

# NOTE(huxuan): Use Flask's error handler instead of the one in flask-restful.
bp_api.handle_exception = partial(Flask.handle_exception, bp_api)
bp_api.handle_user_exception = partial(Flask.handle_user_exception, bp_api)


class APIResponse():

    def __init__(self, status_code=None, message=None, payload=None):
        self.status_code = status_code or code.API_CODE_OK
        self.message = message or code.API_CODE_MESSAGE.get(
            self.status_code, u'Invalid status code.')
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        if self.message is not None:
            rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class APIException(Exception, APIResponse):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self)
        APIResponse.__init__(self, *args, **kwargs)


@bp_api.errorhandler(APIException)
def error_handler(api_exception):
    return jsonify(api_exception.to_dict())


def api_response(*args, **kwargs):
    return jsonify(APIResponse(*args, **kwargs).to_dict())


@bp_api.route('/')
@bp_api.route('/test')
@bp_api.route('/test/response')
def response():
    return api_response(message='APIResponse from {}!'.format(__name__))


@bp_api.route('/test/exception')
def test():
    raise APIException(message='APIException from {}!'.format(__name__))
