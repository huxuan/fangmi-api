#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: huxuan
Email: i(at)huxuan.org
Description: Shared library for FangMi.
"""
from flask import jsonify

API_CODE_OK = 200

API_CODE_MESSAGE = {
    API_CODE_OK: u'OK',
}

class APIResponse():

    def __init__(self, status_code=None, message=None, payload=None):
        self.status_code = status_code or API_CODE_OK
        self.message = message or API_CODE_MESSAGE.get(
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


def api_response(*args, **kwargs):
    return jsonify(APIResponse(*args, **kwargs).to_dict())
