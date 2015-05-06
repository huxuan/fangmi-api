#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: utils.py
Author: huxuan
Email: i(at)huxuan.org
Description: Shared library for FangMi.
"""
from datetime import datetime
from shutil import copyfileobj
from threading import Thread
import cStringIO as StringIO
import hashlib
import os
import re
import requests

from flask import json
from flask import jsonify
from flask.ext.restful import reqparse

from app import app

API_CODE_OK = 200

API_CODE_INVALID = 201
API_CODE_NOT_AUTHORIZED = 202
API_CODE_NOT_FOUND = 203
API_CODE_REQUIRED = 204

API_CODE_SNS_NOT_SUPPORTED = 301

API_CODE_APARTMENT_NOT_FOUND = 1001
API_CODE_APARTMENT_NOT_AUTHORIZED = 1002
API_CODE_CAPTCHA_INVALID = 2001
API_CODE_CAPTCHA_NOT_FOUND = 2002
API_CODE_CAPTCHA_EXCEED_FREQUENCY = 2003
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
    'apartments': '房屋',
    'captchas': '验证码',
    'devices': '设备',
    'devices.count': '设备数量',
    'devices.name': '设备名称',
    'file': '文件',
    'id_number': '身份证号',
    'json': 'Json 数据',
    'major': '专业',
    'messages': '消息',
    'mobile': '手机号',
    'password': '密码',
    'password_confirm': '密码确认',
    'password_new': '新密码',
    'password_new_confirm': '密码确认',
    'password_old': '原始密码',
    'pic_student': '学生证图片',
    'real_name': '姓名',
    'rents': '租房记录',
    'reserve_choices': '预约时间',
    'reserve_choices.date': '预约日期',
    'reserve_choices.time_end': '预约的结束时间',
    'reserve_choices.time_start': '预约的开始时间',
    'reserves': '预约记录',
    'rooms': '房间',
    'rooms.area': '房间面积',
    'rooms.date_entrance': '房间入住时间',
    'rooms.name': '房间名称',
    'rooms.price': '房间价格',
    'schools': '学校',
    'student_id': '学号',
    'tags': '标签',
    'tags.name': '标签名称',
    'username': '用户名',
}


API_CODE_MESSAGE = {
    API_CODE_OK: u'OK',
    API_CODE_INVALID: '{name}不合法。',
    API_CODE_NOT_AUTHORIZED: '您没有操作此{name}的权限。',
    API_CODE_NOT_FOUND: '{name}不存在。',
    API_CODE_REQUIRED: '{name}不能为空。',

    API_CODE_SNS_NOT_SUPPORTED: '不支持{name}社交平台的登录。',

    API_CODE_APARTMENT_NOT_FOUND: '房屋不存在。',
    API_CODE_CAPTCHA_INVALID: u'验证码错误，请确认验证码输入正确。',
    API_CODE_CAPTCHA_NOT_FOUND: u'该手机号无对应验证码，请重新获取。',
    API_CODE_CAPTCHA_EXCEED_FREQUENCY: u'验证码请求频率超过限制，请稍后再试。',
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


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


class APIResponse():

    def __init__(self, status_code=None, message=None, payload=None, **kwargs):
        if 'name' in kwargs and kwargs['name'] in ARGUMENT_NAME:
            kwargs['name'] = ARGUMENT_NAME[kwargs['name']]
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
        if 'Missing required parameter' in error.message:
            raise APIException(API_CODE_REQUIRED, name=self.name)
        if 'not a valid choice' in error.message:
            raise APIException(API_CODE_INVALID, name=self.name)
        if isinstance(error, APIException):
            raise error
        raise APIException(API_CODE_INVALID, name=self.name)

    def parse(self, request):
        result, _found = super(Argument, self).parse(request)
        if not result and self.required:
            raise APIException(API_CODE_REQUIRED, name=self.name)
        return result, _found


class RequestParser(reqparse.RequestParser):
    def __init__(self, argument_class=Argument,
        namespace_class=reqparse.Namespace):
        super(RequestParser, self).__init__(argument_class=argument_class,
            namespace_class=namespace_class)


reqparse.RequestParser = RequestParser


def json_type(data, name='json'):
    try:
        return json.loads(data)
    except:
        raise APIException(API_CODE_INVALID, name=name)


def parser_required(name, data, keys):
    for key in keys:
        if key not in data:
            raise APIException(API_CODE_REQUIRED,
                name='{}.{}'.format(name, key))


def parser_parse(name, data, key_parses):
    for key, parse in key_parses:
        try:
            data[key] = parse(data[key])
        except Exception, e:
            raise APIException(API_CODE_INVALID, name='{}.{}'.format(name, key))
        if hasattr(data[key], 'isoformat'):
            data[key] = data[key].isoformat()
    return data


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
    return datetime.strptime(t, app.config['TIME_FORMAT']).time()


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


MOBILE_PATTERN = re.compile("^1[34578]\d{9}$")


def verify_mobile(mobile):
    if MOBILE_PATTERN.match(mobile):
        return True
    else:
        raise APIException(API_CODE_INVALID, name='mobile')


@async
def send_async_sms(mobile, message):
    payload = {
        'cdkey': app.config['EMY_CDKEY'],
        'password': app.config['EMY_PASSWORD'],
        'phone': mobile,
        'message': message,
    }
    r = requests.post(app.config['EMY_URL'], data=payload)
    return r


def send_captcha_sms(mobile, captcha):
    message = app.config['EMY_MESSAGE'].format(captcha)
    return send_async_sms(mobile, message)


def get_sns_username(username, sns):
    return '_'.join([sns, username])


def verify_sns_username_password(username, password, sns):
    if sns == 'wechat':
        url = 'https://api.weixin.qq.com/sns/auth'
        params = {'access_token': password, 'openid': username}
        res = requests.get(url, params=params)
        return res.json()['errcode'] == 0
    else:
        raise APIException(API_CODE_SNS_NOT_SUPPORTED, name=sns)
