#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for api blueprint.
"""
from flask import Blueprint
from flask import Flask
from flask import jsonify

from .. import models
from .. import utils

bp_api = Blueprint('api', __name__)


@bp_api.route('/')
@bp_api.route('/test')
@bp_api.route('/test/response')
def response():
    return utils.api_response(message='APIResponse from {}!'.format(__name__))


@bp_api.route('/test/exception')
def test():
    raise utils.APIException(message='APIException from {}!'.format(__name__))
