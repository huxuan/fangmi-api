#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for admin.
"""
from flask.ext.admin import Admin
from flask.ext.login import LoginManager

from . import views
from app import app
from app import db
from app import models

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(username):
    return models.Admin.get(username)

admin = Admin(app, name="FangMi Admin",
    index_view=views.MyAdminIndexView(),
    base_template='admin/my_master.html',
    template_mode='bootstrap3',
)
admin.add_view(views.MyModelView(models.Admin, db.session,
    endpoint='admin_admin', category="Model"))
admin.add_view(views.MyModelView(models.User, db.session,
    endpoint='admin_user', category="Model"))
admin.add_view(views.MyModelView(models.School, db.session,
    endpoint='admin_school', category="Model"))
admin.add_view(views.MyModelView(models.Community, db.session,
    endpoint='admin_community', category="Model"))
admin.add_view(views.MyModelView(models.Apartment, db.session,
    endpoint='admin_apartment', category="Model"))
admin.add_view(views.MyModelView(models.ReserveChoice, db.session,
    endpoint='admin_reserve_choice', category="Model"))
admin.add_view(views.MyModelView(models.Room, db.session,
    endpoint='admin_room', category="Model"))
admin.add_view(views.MyModelView(models.Device, db.session,
    endpoint='admin_device', category="Model"))
admin.add_view(views.MyModelView(models.Photo, db.session,
    endpoint='admin_photo', category="Model"))
admin.add_view(views.MyModelView(models.Tag, db.session,
    endpoint='admin_tag', category="Model"))
admin.add_view(views.MyModelView(models.Rent, db.session,
    endpoint='admin_rent', category="Model"))
admin.add_view(views.MyModelView(models.Reserve, db.session,
    endpoint='admin_reserve', category="Model"))
admin.add_view(views.MyModelView(models.Message, db.session,
    endpoint='admin_message', category="Model"))
admin.add_view(views.MyModelView(models.Comment, db.session,
    endpoint='admin_comment', category="Model"))
admin.add_view(views.MyModelView(models.Captcha, db.session,
    endpoint='admin_captcha', category="Model"))
admin.add_view(views.MyModelView(models.Client, db.session,
    endpoint='admin_client', category="Model"))
admin.add_view(views.MyModelView(models.Token, db.session,
    endpoint='admin_token', category="Model"))
