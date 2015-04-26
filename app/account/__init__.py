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
        user = request.oauth.user
        payload = dict(
            user=user.serialize(),
        )
        return utils.api_response(payload=payload)

    @oauth.require_oauth()
    def post(self):
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
