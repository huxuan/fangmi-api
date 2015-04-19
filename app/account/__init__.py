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
from flask.ext.restful import reqparse

from .. import models
from .. import utils
from ..oauth import oauth

account = Blueprint('account', __name__)
api = Api(account)


class RegisterAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('password_confirm', type=str, default='')
        self.parser.add_argument('captcha', type=str, required=True)

    def post(self):
        args = self.parser.parse_args(request)
        models.Captcha.verify(args['username'], args['captcha'])
        utils.check_password_confirm(args['password'], args['password_confirm'])
        models.User.check_not_exist(args['username'])
        user = models.User.create(args['username'], args['password'])
        return utils.api_response(payload=user.serialize())


class PasswordForgetAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('captcha', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('password_confirm', type=str, required=True)

    def post(self):
        args = self.parser.parse_args(request)
        models.Captcha.verify(args['username'], args['captcha'])
        utils.check_password_confirm(args['password'], args['password_confirm'])
        user = models.User.get(args['username'])
        user.change_password(args['password'])
        return utils.api_response()


class PasswordChangeAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('password_old', type=str, required=True)
        self.parser.add_argument('password_new', type=str, required=True)
        self.parser.add_argument('password_new_confirm', type=str,
            required=True)

    @oauth.require_oauth()
    def post(self):
        args = self.parser.parse_args(request)
        utils.check_password_confirm(args['password_new'],
            args['password_new_confirm'])
        user = request.oauth.user
        user.verify_password(args['password_old'])
        user.change_password(args['password_new'])
        return utils.api_response()


api.add_resource(RegisterAPI, '/register')
api.add_resource(PasswordForgetAPI, '/password/forget')
api.add_resource(PasswordChangeAPI, '/password/change')
