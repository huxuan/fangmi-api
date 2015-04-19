#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.py
Author: huxuan
Email: i(at)huxuan.org
Description: Configuration file for FangMi.
"""
# Debug or not
DEBUG = True

# Make jsonfiy encode in utf-8.
JSON_AS_ASCII = False

# Secret key.
SECRET_KEY = 'FangMi_Secret_Key'

# Database & sqlalchemy.
DB_USERNAME = 'fangmi'
DB_PASSWORD = 'fangmi'
DB_SERVER = 'localhost'
DB_NAME = 'fangmi'
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
    DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_NAME)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# The md5 for default avatar.
DEFAULT_AVATAR_MD5 = 'DEFAULT_AVATAR_MD5'

# Data/Time format we use.
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = ' '.join([DATE_FORMAT, TIME_FORMAT])
