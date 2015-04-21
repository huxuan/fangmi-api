#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.py
Author: huxuan
Email: i(at)huxuan.org
Description: Configuration file for FangMi.
"""
import os

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

# The maximun block size we read every time when processing file.
BLOCKSIZE = 65536
# The directory to store uploaded files.
UPLOAD_DIR = 'uploads'
UPLOAD_URL = UPLOAD_DIR
UPLOAD_FOLDER = os.path.realpath(os.path.join(
    os.path.dirname(__file__),
    UPLOAD_DIR,
))
UPLOAD_AVATAR_DIR = 'avatars'
UPLOAD_AVATAR_URL = os.path.join(UPLOAD_URL, UPLOAD_AVATAR_DIR)
UPLOAD_AVATAR_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_AVATAR_DIR,
))
UPLOAD_PIC_STUDENT_DIR = 'students'
UPLOAD_PIC_STUDENT_URL = os.path.join(UPLOAD_URL, UPLOAD_PIC_STUDENT_DIR)
UPLOAD_PIC_STUDENT_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_PIC_STUDENT_DIR,
))
UPLOAD_PIC_PORTAL_DIR = 'portals'
UPLOAD_PIC_PORTAL_URL = os.path.join(UPLOAD_URL, UPLOAD_PIC_PORTAL_DIR)
UPLOAD_PIC_PORTAL_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_PIC_PORTAL_DIR,
))
UPLOAD_SCHOOL_AVATAR_DIR = 'school/avatars'
UPLOAD_SCHOOL_AVATAR_URL = os.path.join(UPLOAD_URL, UPLOAD_SCHOOL_AVATAR_DIR)
UPLOAD_SCHOOL_AVATAR_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_SCHOOL_AVATAR_DIR,
))
UPLOAD_SCHOOL_IMAGE_DIR = 'school/images'
UPLOAD_SCHOOL_IMAGE_URL = os.path.join(UPLOAD_URL, UPLOAD_SCHOOL_IMAGE_DIR)
UPLOAD_SCHOOL_IMAGE_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_SCHOOL_IMAGE_DIR,
))
UPLOAD_COMMUNITY_MAP_DIR = 'maps'
UPLOAD_COMMUNITY_MAP_URL = os.path.join(UPLOAD_URL, UPLOAD_COMMUNITY_MAP_DIR)
UPLOAD_COMMUNITY_MAP_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_COMMUNITY_MAP_DIR,
))
