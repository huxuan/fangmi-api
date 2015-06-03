#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: account.py
Author: huxuan
Email: i(at)huxuan.org
Description: Account related API.
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

account = Blueprint('account', __name__)
api = Api(account)


class AccountAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nickname', default=None)
        self.parser.add_argument('gender', type=inputs.boolean, default=None)
        self.parser.add_argument('horoscope', type=int, choices=range(12),
            default=None)
        self.parser.add_argument('status', default=None)
        self.parser.add_argument('avatar',
            type=datastructures.FileStorage,
            location='files',
        )

    @oauth.require_oauth()
    def get(self):
        """ 获取当前登录用户的信息

        **Example Request**:

        .. sourcecode:: http

            GET /api/account
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 10,
                  "id_number": null,
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "u1",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": null,
                  "real_name": null,
                  "school": null,
                  "status": "I'm u1",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :<header Authorization: OAuth access_token
        :>json string username: 登录用户的用户名
        :>json string nickname: 登录用户的昵称
        :>json string avatar: 登录用户的头像 url 地址
        :>json string status: 登录用户的个性签名
        :>json string birthday: 登录用户的生日
        :>json int horoscope: 登录用户的星座，为星座对应序号
        :>json bool gender: 登录用户的性别，0:女，1:男
        :>json string mobile: 登录用户的手机号
        :>json int num_fav_apartments: 登录用户收藏的房间数目
        :>json int num_unread_messages: 登录用户的未读消息数目
        :>json boolean is_confirmed: 登录用户是否已通过真实姓名认证
        :>json boolean is_student: 登录用户是否通过学生认证
        :>json string created_at: 登录用户的创建时间
        :>json string deleted: 登录用户是否已被删除
        :>json string shool: 登录用户的学校
        :>json string major: 登录用户的专业
        :>json string student_id: 登录用户的学号
        :>json string pic_student: 登录用户学生证照片 url 地址
        :>json string pic_portal: 登录用户学校门户照片 url 地址
        :>json string real_name: 登录用户的真实姓名
        :>json string id_number: 登录用户的身份证号码
        """
        user = request.oauth.user
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
        """ 更新当前登录用户的信息

        **Example Request**:

        .. sourcecode:: http

            POST /api/account
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="nickname"

            new_nickname
            --AaB03x
            Content-Disposition: form-data; name="gender"

            true
            --AaB03x
            Content-Disposition: form-data; name="horoscope"

            6
            --AaB03x
            Content-Disposition: form-data; name="status"

            new_status
            --AaB03x
            Content-Disposition: form-data; name="avatar";
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of avatar ...
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "[relative url path for new avatar]",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": null,
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": null,
                  "real_name": null,
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :<header Authorization: OAuth access_token
        :form nickname: 用户的新昵称
        :form gender: 用户的新性别
        :form horoscope: 用户的新星座，为星座对应序号
        :form status: 用户的新个性签名
        :form avatar: 用户的新头像
        :>json string username: 登录用户的用户名
        :>json string nickname: 登录用户的昵称
        :>json string avatar: 登录用户的头像 url 地址
        :>json string status: 登录用户的个性签名
        :>json string birthday: 登录用户的生日
        :>json int horoscope: 登录用户的星座，为星座对应序号
        :>json bool gender: 登录用户的性别，0:女，1:男
        :>json string mobile: 登录用户的手机号
        :>json int num_fav_apartments: 登录用户收藏的房间数目
        :>json int num_unread_messages: 登录用户的未读消息数目
        :>json boolean is_confirmed: 登录用户是否已通过真实姓名认证
        :>json boolean is_student: 登录用户是否通过学生认证
        :>json string created_at: 登录用户的创建时间
        :>json string deleted: 登录用户是否已被删除
        :>json string shool: 登录用户的学校
        :>json string major: 登录用户的专业
        :>json string student_id: 登录用户的学号
        :>json string pic_student: 登录用户学生证照片 url 地址
        :>json string pic_portal: 登录用户学校门户照片 url 地址
        :>json string real_name: 登录用户的真实姓名
        :>json string id_number: 登录用户的身份证号码
        """
        args = self.parser.parse_args(request)
        user = request.oauth.user
        user.set(**args)
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)


class RegisterAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('password', required=True)
        self.parser.add_argument('password_confirm', default='')
        self.parser.add_argument('captcha', required=True)

    def post(self):
        """ 注册新用户

        **Example Request**:

        .. sourcecode:: http

            POST /api/account/register
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="username"

            username
            --AaB03x
            Content-Disposition: form-data; name="password"

            password
            --AaB03x
            Content-Disposition: form-data; name="password_confirm"

            password_confirm
            --AaB03x
            Content-Disposition: form-data; name="captcha"

            123456
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": null,
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": null,
                  "real_name": null,
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :form username: 用户的用户名
        :form password: 用户的密码
        :form password_confirm: 用户的密码确认
        :form captcha: 手机验证码
        :>json string username: 用户的用户名
        :>json string nickname: 用户的昵称
        :>json string avatar: 用户的头像 url 地址
        :>json string status: 用户的个性签名
        :>json string birthday: 用户的生日
        :>json int horoscope: 用户的星座，为星座对应序号
        :>json bool gender: 用户的性别，0:女，1:男
        :>json string mobile: 用户的手机号
        :>json int num_fav_apartments: 用户收藏的房间数目
        :>json int num_unread_messages: 用户的未读消息数目
        :>json boolean is_confirmed: 用户是否已通过真实姓名认证
        :>json boolean is_student: 用户是否通过学生认证
        :>json string created_at: 用户的创建时间
        :>json string deleted: 用户是否已被删除
        :>json string shool: 用户的学校
        :>json string major: 用户的专业
        :>json string student_id: 用户的学号
        :>json string pic_student: 用户学生证照片 url 地址
        :>json string pic_portal: 用户学校门户照片 url 地址
        :>json string real_name: 用户的真实姓名
        :>json string id_number: 用户的身份证号码
        """
        args = self.parser.parse_args(request)
        models.Captcha.verify(args['username'], args['captcha'])
        utils.check_password_confirm(args['password'], args['password_confirm'])
        models.User.check_not_exist(args['username'])
        user = models.User.create(args['username'], args['password'])
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)


class PasswordForgetAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('captcha', required=True)
        self.parser.add_argument('password', required=True)
        self.parser.add_argument('password_confirm', required=True)

    def post(self):
        """ 重置用户密码

        **Example Request**:

        .. sourcecode:: http

            POST /api/account/password/forget
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="username"

            username
            --AaB03x
            Content-Disposition: form-data; name="password"

            password
            --AaB03x
            Content-Disposition: form-data; name="password_confirm"

            password_confirm
            --AaB03x
            Content-Disposition: form-data; name="captcha"

            123456
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": null,
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": "/uploads/students/58/7c/36119c43e7383b739e6093c23150",
                  "real_name": null,
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :form username: 用户的用户名
        :form password: 用户的新密码
        :form password_confirm: 用户的新密码确认
        :form captcha: 手机验证码
        :>json string username: 用户的用户名
        :>json string nickname: 用户的昵称
        :>json string avatar: 用户的头像 url 地址
        :>json string status: 用户的个性签名
        :>json string birthday: 用户的生日
        :>json int horoscope: 用户的星座，为星座对应序号
        :>json bool gender: 用户的性别，0:女，1:男
        :>json string mobile: 用户的手机号
        :>json int num_fav_apartments: 用户收藏的房间数目
        :>json int num_unread_messages: 用户的未读消息数目
        :>json boolean is_confirmed: 用户是否已通过真实姓名认证
        :>json boolean is_student: 用户是否通过学生认证
        :>json string created_at: 用户的创建时间
        :>json string deleted: 用户是否已被删除
        :>json string shool: 用户的学校
        :>json string major: 用户的专业
        :>json string student_id: 用户的学号
        :>json string pic_student: 用户学生证照片 url 地址
        :>json string pic_portal: 用户学校门户照片 url 地址
        :>json string real_name: 用户的真实姓名
        :>json string id_number: 用户的身份证号码
        """
        args = self.parser.parse_args(request)
        models.Captcha.verify(args['username'], args['captcha'])
        utils.check_password_confirm(args['password'], args['password_confirm'])
        user = models.User.get(args['username'])
        user.change_password(args['password'])
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)


class PasswordChangeAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('password_old', required=True)
        self.parser.add_argument('password_new', required=True)
        self.parser.add_argument('password_new_confirm', required=True)

    @oauth.require_oauth()
    def post(self):
        """ 修改用户密码

        **Example Request**:

        .. sourcecode:: http

            POST /api/account/password/change
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="password_old"

            password_old
            --AaB03x
            Content-Disposition: form-data; name="password_new"

            password_new
            --AaB03x
            Content-Disposition: form-data; name="password_new_confirm"

            password_new_confirm
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": null,
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": "/uploads/students/58/7c/36119c43e7383b739e6093c23150",
                  "real_name": null,
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :<header Authorization: OAuth access_token
        :form password_old: 用户的旧密码
        :form password_new: 用户的新密码
        :form password_new_confirm: 用户的新密码确认
        :form captcha: 手机验证码
        :>json string username: 用户的用户名
        :>json string nickname: 用户的昵称
        :>json string avatar: 用户的头像 url 地址
        :>json string status: 用户的个性签名
        :>json string birthday: 用户的生日
        :>json int horoscope: 用户的星座，为星座对应序号
        :>json bool gender: 用户的性别，0:女，1:男
        :>json string mobile: 用户的手机号
        :>json int num_fav_apartments: 用户收藏的房间数目
        :>json int num_unread_messages: 用户的未读消息数目
        :>json boolean is_confirmed: 用户是否已通过真实姓名认证
        :>json boolean is_student: 用户是否通过学生认证
        :>json string created_at: 用户的创建时间
        :>json string deleted: 用户是否已被删除
        :>json string shool: 用户的学校
        :>json string major: 用户的专业
        :>json string student_id: 用户的学号
        :>json string pic_student: 用户学生证照片 url 地址
        :>json string pic_portal: 用户学校门户照片 url 地址
        :>json string real_name: 用户的真实姓名
        :>json string id_number: 用户的身份证号码
        """
        args = self.parser.parse_args(request)
        utils.check_password_confirm(args['password_new'],
            args['password_new_confirm'])
        user = request.oauth.user
        user.verify_password(args['password_old'])
        user.change_password(args['password_new'])
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)


class ApplyConfirmedAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('real_name', required=True)
        self.parser.add_argument('id_number', required=True)

    @oauth.require_oauth()
    def post(self):
        """ 申请真实姓名认证

        **Example Request**:

        .. sourcecode:: http

            POST /api/account/apply/confirmed
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="real_name"

            real_name_new
            --AaB03x
            Content-Disposition: form-data; name="id_number"

            id_number_new
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": "id_number_new",
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": "/uploads/students/58/7c/36119c43e7383b739e6093c23150",
                  "real_name": "real_name_new",
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :<header Authorization: OAuth access_token
        :form real_name: 用户的真实姓名
        :form id_number: 用户的身份证号码
        :>json string username: 用户的用户名
        :>json string nickname: 用户的昵称
        :>json string avatar: 用户的头像 url 地址
        :>json string status: 用户的个性签名
        :>json string birthday: 用户的生日
        :>json int horoscope: 用户的星座，为星座对应序号
        :>json bool gender: 用户的性别，0:女，1:男
        :>json string mobile: 用户的手机号
        :>json int num_fav_apartments: 用户收藏的房间数目
        :>json int num_unread_messages: 用户的未读消息数目
        :>json boolean is_confirmed: 用户是否已通过真实姓名认证
        :>json boolean is_student: 用户是否通过学生认证
        :>json string created_at: 用户的创建时间
        :>json string deleted: 用户是否已被删除
        :>json string shool: 用户的学校
        :>json string major: 用户的专业
        :>json string student_id: 用户的学号
        :>json string pic_student: 用户学生证照片 url 地址
        :>json string pic_portal: 用户学校门户照片 url 地址
        :>json string real_name: 用户的真实姓名
        :>json string id_number: 用户的身份证号码
        """
        args = self.parser.parse_args(request)
        user = request.oauth.user
        user.set(**args)
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)

class ApplyStudentAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('real_name', required=True)
        self.parser.add_argument('id_number', required=True)
        self.parser.add_argument('school', required=True)
        self.parser.add_argument('major', required=True)
        self.parser.add_argument('student_id', required=True)
        self.parser.add_argument('pic_student', required=True,
            type=datastructures.FileStorage, location='files',
        )

    @oauth.require_oauth()
    def post(self):
        """ 申请学生认证

        **Example Request**:

        .. sourcecode:: http

            POST /api/account/apply/confirmed
            Authorization: Bearer YSj3GtbBvEWmFkL0hhH26PWQrpbSef
            Content-Type: multipart/form-data; boundary=AaB03x

            --AaB03x
            Content-Disposition: form-data; name="real_name"

            real_name_new
            --AaB03x
            Content-Disposition: form-data; name="id_number"

            id_number_new
            --AaB03x
            Content-Disposition: form-data; name="school"

            school_new
            --AaB03x
            Content-Disposition: form-data; name="major"

            major_new
            --AaB03x
            Content-Disposition: form-data; name="student_id"

            student_id_new
            --AaB03x
            Content-Disposition: form-data; name="pic_student";
            Content-Type: image/jpeg
            Content-Transfer-Encoding: binary

            ... contents of pic_student ...
            --AaB03x--

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
                "user": {
                  "avatar": "/uploads/avatars/58/7c/36119c43e7383b739e6093c23150",
                  "birthday": null,
                  "created_at": "2015-05-29T10:53:42",
                  "deleted": false,
                  "gender": true,
                  "horoscope": 6,
                  "id_number": "id_number_new",
                  "is_confirmed": false,
                  "is_student": false,
                  "major": null,
                  "mobile": "u1",
                  "nickname": "new_nickname",
                  "num_fav_apartments": 1,
                  "num_unread_messages": 10,
                  "pic_portal": null,
                  "pic_student": "/uploads/students/58/7c/36119c43e7383b739e6093c23150",
                  "real_name": "real_name_new",
                  "school": null,
                  "status": "new_status",
                  "student_id": null,
                  "username": "u1"
                }
            }

        :<header Authorization: OAuth access_token
        :form real_name: 用户的真实姓名
        :form id_number: 用户的身份证号码
        :form school: 用户的学校
        :form major: 用户的专业
        :form student_id: 用户的学号
        :form pic_student: 用户的学生证照片
        :>json string username: 用户的用户名
        :>json string nickname: 用户的昵称
        :>json string avatar: 用户的头像 url 地址
        :>json string status: 用户的个性签名
        :>json string birthday: 用户的生日
        :>json int horoscope: 用户的星座，为星座对应序号
        :>json bool gender: 用户的性别，0:女，1:男
        :>json string mobile: 用户的手机号
        :>json int num_fav_apartments: 用户收藏的房间数目
        :>json int num_unread_messages: 用户的未读消息数目
        :>json boolean is_confirmed: 用户是否已通过真实姓名认证
        :>json boolean is_student: 用户是否通过学生认证
        :>json string created_at: 用户的创建时间
        :>json string deleted: 用户是否已被删除
        :>json string shool: 用户的学校
        :>json string major: 用户的专业
        :>json string student_id: 用户的学号
        :>json string pic_student: 用户学生证照片 url 地址
        :>json string pic_portal: 用户学校门户照片 url 地址
        :>json string real_name: 用户的真实姓名
        :>json string id_number: 用户的身份证号码
        """
        args = self.parser.parse_args(request)
        user = request.oauth.user
        user.set(**args)
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)


api.add_resource(AccountAPI, '')
api.add_resource(RegisterAPI, '/register')
api.add_resource(PasswordForgetAPI, '/password/forget')
api.add_resource(PasswordChangeAPI, '/password/change')
api.add_resource(ApplyConfirmedAPI, '/apply/confirmed')
api.add_resource(ApplyStudentAPI, '/apply/student')
