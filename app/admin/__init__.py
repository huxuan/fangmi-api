#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for admin blueprints.
"""
from flask.ext.admin import Admin

from app import app

admin = Admin(app, name="FangMi Admin")
