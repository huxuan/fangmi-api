#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for oauth blueprint.
"""

from flask import Blueprint

oauth = Blueprint('oauth', __name__)

@oauth.route('/')
@oauth.route('/test')
def test():
    return 'Hello world from {}!'.format(__name__)
