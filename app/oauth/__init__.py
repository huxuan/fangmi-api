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

from .. import app
from app import models

oauth = Blueprint('oauth', __name__)


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

oauthlib = OAuth2Provider(app)
oauthlib._validator = PasswordCredentialRequestValidator()


@oauth.route('/token', methods=['POST'])
@oauthlib.token_handler
def access_token():
    return None


@oauth.route('/me')
@oauthlib.require_oauth()
def me():
    return jsonify(message="Logged In!")


@oauth.route('/')
@oauth.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
