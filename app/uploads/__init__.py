#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Uploads related API.
"""
import os.path

from flask import Blueprint
from flask import request
from flask import safe_join
from flask import send_file
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from .. import app
from .. import utils
from ..oauth import oauth
from ..utils import reqparse

uploads = Blueprint('uploads', __name__)
api = Api(uploads)


class UploadsAPI(Resource):
    def get(self, file_path):
        file_path = safe_join(app.config['UPLOAD_FOLDER'], file_path)
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            raise utils.APIException(utils.API_CODE_NOT_FOUND, name='file')


api.add_resource(UploadsAPI, '/<path:file_path>')
