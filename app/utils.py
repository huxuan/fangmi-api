#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: huxuan
Email: i(at)huxuan.org
Description: Shared library for FangMi.
"""
from shutil import copyfileobj
import cStringIO as StringIO
import hashlib
import os

from flask import json
from flask import jsonify
from flask.ext.restful import reqparse

from app import app

API_CODE_OK = 200

API_CODE_INVALID = 201
API_CODE_NOT_FOUND = 202
API_CODE_REQUIRED = 203

API_CODE_APARTMENT_NOT_FOUND = 1001
API_CODE_APARTMENT_NOT_AUTHORIZED = 1002
API_CODE_CAPTCHA_INVALID = 2001
API_CODE_CAPTCHA_NOT_FOUND = 2002
API_CODE_COMMUNITY_NOT_FOUND = 3001
API_CODE_MESSAGE_NOT_FOUND = 4001
API_CODE_PASSWORD_CONFIRM_INVALID = 5001
API_CODE_PASSWORD_INVALID = 5002
API_CODE_RENT_NOT_FOUND = 6001
API_CODE_RESERVE_NOT_FOUND = 7001
API_CODE_SCHOOL_NOT_FOUND = 8001
API_CODE_USER_DUPLICATE = 9001
API_CODE_USER_NOT_AUTHORIZED = 9002
API_CODE_USER_NOT_FOUND = 9003

ARGUMENT_NAME = {
    'json': 'Json 数据',
    'password': '密码',
    'username': '用户名',
}


API_CODE_MESSAGE = {
    API_CODE_OK: u'OK',
    API_CODE_REQUIRED: '{name}不能为空。',
    API_CODE_INVALID: '{name}不合法。',
    API_CODE_NOT_FOUND: '{name}不存在。',
    API_CODE_APARTMENT_NOT_FOUND: '房屋不存在。',
    API_CODE_APARTMENT_NOT_AUTHORIZED: '您没有操作此房屋的权限。',
    API_CODE_CAPTCHA_INVALID: u'验证码错误，请确认验证码输入正确。',
    API_CODE_CAPTCHA_NOT_FOUND: u'该手机号无对应验证码，请重新获取。',
    API_CODE_COMMUNITY_NOT_FOUND: u'小区不存在。',
    API_CODE_MESSAGE_NOT_FOUND: '消息不存在。',
    API_CODE_PASSWORD_CONFIRM_INVALID: u'确认密码不一致。',
    API_CODE_PASSWORD_INVALID: u'密码错误。',
    API_CODE_RENT_NOT_FOUND: u'租房记录不存在。',
    API_CODE_RESERVE_NOT_FOUND: '预约记录不存在。',
    API_CODE_SCHOOL_NOT_FOUND: u'学校不存在。',
    API_CODE_USER_DUPLICATE: u'用户已存在。',
    API_CODE_USER_NOT_AUTHORIZED: u'用户验证失败。',
    API_CODE_USER_NOT_FOUND: u'用户不存在。',
}


class APIResponse():

    def __init__(self, status_code=None, message=None, payload=None, **kwargs):
        self.status_code = status_code or API_CODE_OK
        self.message = message or API_CODE_MESSAGE[self.status_code]
        self.message = self.message.format(**kwargs)
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


class Argument(reqparse.Argument):

    def handle_validation_error(self, error):
        self.arg_name = ARGUMENT_NAME.get(self.name) or self.name
        if 'Missing required parameter' in error.message:
            raise APIException(API_CODE_REQUIRED, name=self.arg_name)
        if 'not a valid choice' in error.message:
            raise APIException(API_CODE_INVALID, name=self.arg_name)
        super(Argument, self).handle_validation_error(error)

    def parse(self, request):
        result, _found = super(Argument, self).parse(request)
        if not result and self.required:
            raise APIException(API_CODE_REQUIRED, name=self.arg_name)

class RequestParser(reqparse.RequestParser):
    def __init__(self):
        super(RequestParser, self).__init__(argument_class=Argument)

reqparse.RequestParser = RequestParser


def json_type(data, name='json'):
    try:
        return json.loads(data)
    except:
        raise APIException(API_CODE_INVALID, name=name)


def check_password_confirm(password, password_confirm):
    if password != password_confirm:
        raise APIException(API_CODE_PASSWORD_CONFIRM_INVALID)


def strfdate(d):
    """ Convert from datetime.date object to string. """
    return d.strftime(app.config['DATE_FORMAT'])


def strftime(t):
    """ Convert from datetime.time object to string. """
    return t.strftime(app.config['TIME_FORMAT'])


def strfdatetime(dt):
    """ Convert from datetime.datetime object to string. """
    return dt.strftime(app.config['DATETIME_FORMAT'])


def strpdate(d):
    """ Convert from string to datetime.date object. """
    return datetime.strptime(d, app.config['DATE_FORMAT']).date()


def strptime(t):
    """ Convert from string to datetime.time object. """
    return time.strptime(t, app.config['TIME_FORMAT']).time()


def strpdatetime(dt):
    """ Convert from string to datetime.datetime object. """
    return datetime.strptime(dt, app.config['DATETIME_FORMAT'])


def get_stringio_and_md5_from_stream(stream):
    hasher = hashlib.md5()
    stringio = StringIO.StringIO()
    buf = stream.read(app.config['BLOCKSIZE'])
    while len(buf) > 0:
        hasher.update(buf)
        stringio.write(buf)
        buf = stream.read(app.config['BLOCKSIZE'])
    stringio.seek(0)
    return stringio, hasher.hexdigest()


def get_path_from_md5(folder, file_md5):
    file_path = '/'.join([file_md5[:2], file_md5[2:4], file_md5[4:]])
    file_path = os.path.join(folder, file_path)
    return os.path.realpath(file_path)


def get_url_from_md5(folder, file_md5):
    if file_md5:
        return '/'.join(['', folder, file_md5[:2], file_md5[2:4], file_md5[4:]])
    else:
        return None


def save_file(stream, folder):
    if stream:
        file_stringio, file_md5 = get_stringio_and_md5_from_stream(stream)
        file_path = get_path_from_md5(folder, file_md5)
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.isfile(file_path):
            with open(file_path, 'wb') as fout:
                copyfileobj(file_stringio, fout, app.config['BLOCKSIZE'])
        return file_md5
    else:
        return ""
