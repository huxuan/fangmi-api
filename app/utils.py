#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: huxuan
Email: i(at)huxuan.org
Description: Shared library for FangMi.
"""
from flask import jsonify

from app import app

API_CODE_OK = 200
API_CODE_CAPTCHA_NOT_FOUND = 1001
API_CODE_CAPTCHA_INVALID = 1002
API_CODE_PASSWORD_CONFIRM_INVALID = 2001
API_CODE_USER_EXIST = 3001
API_CODE_USER_NOT_FOUND = 3002

API_CODE_MESSAGE = {
    API_CODE_OK: u'OK',
    API_CODE_CAPTCHA_NOT_FOUND: u'该手机号无对应验证码，请重新获取。',
    API_CODE_CAPTCHA_INVALID: u'验证码错误，请确认验证码输入正确。',
    API_CODE_PASSWORD_CONFIRM_INVALID: u'确认密码不一致。',
    API_CODE_USER_EXIST: u'用户已存在。',
    API_CODE_USER_NOT_FOUND: u'用户不存在。',
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


def check_password_confirm(password, password_confirm):
    if password != password_confirm:
        raise APIException(API_CODE_PASSWORD_CONFIRM_INVALID)


def convert_date(date):
    return date.strftime(app.config['DATE_FORMAT'])


def convert_time(time):
    return time.strftime(app.config['TIME_FORMAT'])


def convert_datetime(datetime):
    return datetime.strftime(app.config['DATETIME_FORMAT'])
