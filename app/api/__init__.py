#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for api blueprint.
"""
from flask import Blueprint

from .. import app
from app import models

bp_api = Blueprint('api', __name__)

@bp_api.route('/')
@bp_api.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
