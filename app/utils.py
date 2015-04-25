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

from flask import jsonify
from flask.ext.restful import reqparse

from app import app

API_CODE_OK = 200
API_CODE_NULL = 201
API_CODE_REQUIRED = 202
API_CODE_INVALID = 203
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

API_CODE_MESSAGE = {
    API_CODE_OK: u'OK',
    API_CODE_NULL: '字段不能为空。',
    API_CODE_REQUIRED: '字段为必需字段。',
    API_CODE_INVALID: '字段不合法。',
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


class Argument(reqparse.Argument):
    def __init__(self, name, default=None, dest=None, required=False,
        ignore=False, type=reqparse.text_type, location=('json', 'values',),
        choices=(), action='store', help=None, operators=('=',),
        case_sensitive=True, nullable=False):
        self.nullable = nullable
        super(Argument, self).__init__(name, default=default, dest=dest,
            required=required, ignore=ignore, type=type, location=location,
            choices=choices, action=action, help=help, operators=operators,
            case_sensitive=case_sensitive)

    def handle_validation_error(self, error):
        pass

    def parse(self, request):
        result, _found = super(Argument, self).parse(request)
        if not result and not self.nullable:
            raise APIException(API_CODE_NULL, msg_params=self.name)
        if not result and self.required:
            raise APIException(API_CODE_REQUIRED, msg_params=self.name)
        if self.choices and result not in self.choices:
            raise APIException(API_CODE_INVALID, msg_params=self.name)

class RequestParser(reqparse.RequestParser):
    def __init__(self):
        super(RequestParser, self).__init__(argument_class=Argument)

reqparse.RequestParser = RequestParser


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
