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
    endpoint='admin_admin'))
admin.add_view(views.MyModelView(models.User, db.session,
    endpoint='admin_user'))
admin.add_view(views.MyModelView(models.School, db.session,
    endpoint='admin_school'))
admin.add_view(views.MyModelView(models.Community, db.session,
    endpoint='admin_community'))
admin.add_view(views.MyModelView(models.Apartment, db.session,
    endpoint='admin_apartment'))
admin.add_view(views.MyModelView(models.ReserveChoice, db.session,
    endpoint='admin_reserve_choice'))
admin.add_view(views.MyModelView(models.Room, db.session,
    endpoint='admin_room'))
admin.add_view(views.MyModelView(models.Device, db.session,
    endpoint='admin_device'))
admin.add_view(views.MyModelView(models.Photo, db.session,
    endpoint='admin_photo'))
admin.add_view(views.MyModelView(models.Tag, db.session,
    endpoint='admin_tag'))
admin.add_view(views.MyModelView(models.Rent, db.session,
    endpoint='admin_rent'))
admin.add_view(views.MyModelView(models.Reserve, db.session,
    endpoint='admin_reserve'))
admin.add_view(views.MyModelView(models.Message, db.session,
    endpoint='admin_message'))
admin.add_view(views.MyModelView(models.Comment, db.session,
    endpoint='admin_comment'))
admin.add_view(views.MyModelView(models.Captcha, db.session,
    endpoint='admin_captcha'))
admin.add_view(views.MyModelView(models.Client, db.session,
    endpoint='admin_client'))
admin.add_view(views.MyModelView(models.Token, db.session,
    endpoint='admin_token'))
