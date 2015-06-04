#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for oauth blueprint.
"""

from flask import Blueprint
from flask import jsonify
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.provider import OAuth2RequestValidator

from .. import models
from .. import utils

bp_oauth = Blueprint('oauth', __name__)
oauth = OAuth2Provider()


@bp_oauth.record_once
def on_load(state):
    oauth.init_app(state.app)

class PasswordCredentialRequestValidator(OAuth2RequestValidator):
    """ A custom OAuth2 Request Validator based on the Client, User
        and Token models. Only useful for Resource Owner Password Credential
        validation.

        :param OAuth2RequestValidator: Overrides the OAuth2RequestValidator.
    """
    def __init__(self):
        self._clientgetter = models.Client.getter
        self._usergetter = models.User.getter
        self._tokengetter = models.Token.getter
        self._tokensetter = models.Token.setter


oauth._validator = PasswordCredentialRequestValidator()

@oauth.invalid_response
def invalid_require_oauth(request):
    raise utils.APIException(utils.API_CODE_USER_NOT_AUTHORIZED)

@bp_oauth.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    """ 用户登录

    **Example Request**:

    .. sourcecode:: http

        POST /api/oauth/token
        grant_type=password&client_id=fangmi-web&username=u2&password=pwd2

        POST /api/oauth/token
        grant_type=password&client_id=fangmi-web&username=<openid>&\
pass=<access_token>&sns=wechat

    **Example Response**:

    .. sourcecode:: http

        {
            "access_token": "YSj3GtbBvEWmFkL0hhH26PWQrpbSef",
            "token_type": "Bearer",
            "refresh_token": "<refresh_token>",
            "scope": ""
        }

    :query string grant_type: **Required** 验证方式，暂时只支持密码，所以必须填\
``password``
    :query string client_id: **Required** 终端 ID，目前可以使用的有 \
``fangmi-web``, ``fangmi-ios``, ``fangmi-android``.
    :query string username: **Required** 用户名，微信登录对应微信里的openid
    :query string password: **Required** 密码，微信登录对应微信里的 access_token
    :query string sns: 登录方式，默认为空可不填指代普通网站登录，``wechat`` \
对应微信的登录
    :>json string access_token: 验证 token，用于需要验证的请求
    :>json string token_type: token 的类别
    :>json string refresh_token: 密码认证方式用不到
    :>json string scope: 权限范围，默认全部开放，我们不需要过多细分
    """
    return None


@bp_oauth.route('/me')
@oauth.require_oauth()
def me():
    return utils.api_response(payload={u'status': u'登录成功！'})


@bp_oauth.route('/')
@bp_oauth.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
