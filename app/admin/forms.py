#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: forms.py
Author: huxuan
Email: i(at)huxuan.org
Description: Form definition for admin.
"""
from wtforms import fields
from wtforms import form
from wtforms import validators

from app import models

class LoginForm(form.Form):
    username = fields.StringField(label=u'用户名',
        validators=[validators.required()],
    )
    password = fields.PasswordField(u'密码',
        validators=[validators.required()],
    )

    def validate_username(self, field):
        self.admin_user = models.Admin.get(self.username.data)
        self.admin_user.verify_password(self.password.data)
