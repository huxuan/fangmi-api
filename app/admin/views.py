#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: views.py
Author: huxuan
Email: i(at)huxuan.org
Description: Views for admin
"""
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask.ext.admin import AdminIndexView
from flask.ext.admin import BaseView
from flask.ext.admin import expose
from flask.ext.admin import helpers
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user

from . import forms


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = forms.LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            login_user(form.admin_user)

        if current_user.is_authenticated():
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))


class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('.login', next=request.url))

class MyModelView(ModelView, MyView):
    column_display_pk = True
    column_hide_backrefs = False
