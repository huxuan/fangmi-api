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
    return None


@bp_oauth.route('/me')
@oauth.require_oauth()
def me():
    return utils.api_response(payload={u'status': u'登录成功！'})


@bp_oauth.route('/')
@bp_oauth.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
