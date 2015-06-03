#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Captcha related API.
"""
from datetime import date

from flask import Blueprint
from flask import request
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import inputs
from flask.ext.restful import reqparse

from .. import models
from .. import utils
from ..oauth import oauth
from ..utils import reqparse

captcha = Blueprint('captcha', __name__)
api = Api(captcha)


class CaptchaAPI(Resource):

    def post(self):
        """ 发送验证码

        **Example Request**:

        .. sourcecode:: http

            POST /api/captcha
            mobile=1

        **Example Response**:

        .. sourcecode:: http

            {
                "message": "OK",
                "status_code": 200,
            }

        :query string mobile: 手机号
        :>json string message: 可能的错误信息
        :>json int status_code: 状态代码
        """
        parser = reqparse.RequestParser()
        parser.add_argument('mobile', required=True)
        args = parser.parse_args(request)
        captcha = models.Captcha.create(args['mobile'])
        return utils.api_response()


api.add_resource(CaptchaAPI, '')
