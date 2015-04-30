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
from flask import session
from flask import url_for
from flask.ext.admin import AdminIndexView
from flask.ext.admin import BaseView
from flask.ext.admin import expose
from flask.ext.admin import helpers
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user
from jinja2 import Markup

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
    column_auto_select_related = True


class StudentConfrimModelView(MyModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_descriptions = dict(
        is_student=u'勾号(True)表示已认证<br>减号(False)表示未认证',
    )
    column_editable_list = ('is_student', )
    column_filters = ('username', 'school', 'major', 'student_id', 'is_student')
    column_formatters = dict(
        pic_student_md5=lambda v, c, m, p:
            Markup('<img src="{}">'.format(m.pic_student)),
    )
    column_labels = dict(username=u'用户名', school=u'学校', major=u'专业',
        student_id=u'学号', pic_student_md5=u'学生证照片',
        is_student=u'是否已认证')
    column_list = ('username', 'school', 'major', 'student_id',
        'pic_student_md5', 'is_student')
    column_searchable_list = ('username', 'school', 'major', 'student_id')
