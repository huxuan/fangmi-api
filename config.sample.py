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
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# The md5 for default avatar.
DEFAULT_AVATAR_MD5 = '587c36119c43e7383b739e6093c23150'

# Data/Time format we use.
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = ' '.join([DATE_FORMAT, TIME_FORMAT])

# Whoosh / Text Search related.
WHOOSH_DIR = 'whoosh_index'
WHOOSH_BASE = os.path.realpath(os.path.join(
    os.path.dirname(__file__),
    WHOOSH_DIR,
))
from jieba.analyse import ChineseAnalyzer
WHOOSH_ANALYZER = ChineseAnalyzer()

# EMY Messaeg
EMY_URL = 'http://sdk4report.eucp.b2m.cn:8080/sdkproxy/sendsms.action'
EMY_CDKEY = ''
EMY_PASSWORD = ''
EMY_MESSAGE = u'【房蜜科技】您的验证码为{}，感谢您使用房蜜。'
EMY_TIMEDELTA_SECONDS = 60

# The maximum content size when uploading.
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
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
UPLOAD_CONTRACT_DIR = 'contracts'
UPLOAD_CONTRACT_URL = os.path.join(UPLOAD_URL, UPLOAD_CONTRACT_DIR)
UPLOAD_CONTRACT_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_CONTRACT_DIR,
))
UPLOAD_PHOTO_DIR = 'photos'
UPLOAD_PHOTO_URL = os.path.join(UPLOAD_URL, UPLOAD_PHOTO_DIR)
UPLOAD_PHOTO_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_PHOTO_DIR,
))
UPLOAD_MESSAGE_DIR = 'messages'
UPLOAD_MESSAGE_URL = os.path.join(UPLOAD_URL, UPLOAD_MESSAGE_DIR)
UPLOAD_MESSAGE_FOLDER = os.path.realpath(os.path.join(
    UPLOAD_FOLDER,
    UPLOAD_MESSAGE_DIR,
))
