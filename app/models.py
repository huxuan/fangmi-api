#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: models.py
Author: huxuan
Email: i(at)huxuan.org
Description: Models for FangMi API.
"""
from datetime import date
from datetime import datetime

from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.declarative import ConcreteBase

from app import app
from app import db

schools_communities = db.Table('schools_communities',
    db.Column('school_id', db.Integer, db.ForeignKey('school.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
)


apartments_tags = db.Table('apartments_tags',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartment.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


apartments_devices = db.Table('apartments_devices',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartment.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id')),
)


apartments_photos = db.Table('apartments_photos',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartment.id')),
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Authentication related.
    username = db.Column(db.String(11), nullable=False, unique=True, index=True)
    password = db.Column(db.String(32), nullable=False)

    # Online Profile.
    nickname = db.Column(db.String(64), nullable=False, unique=True, index=True)
    avatar = db.Column(db.String(32), default=app.config['DEFAULT_AVATAR_MD5'])
    status = db.Column(db.Text)
    birthday = db.Column(db.Date, default=date.today)
    horoscope = db.Column(db.SmallInteger)
    gender = db.Column(db.Boolean)

    # Personal Information.
    name = db.Column(db.String(16))
    mobile = db.Column(db.String(11))
    id_number = db.Column(db.String(18))
    school = db.Column(db.String(32))
    major = db.Column(db.String(32))
    student_id = db.Column(db.String(32))
    pic_student = db.Column(db.String(32))
    pic_portal = db.Column(db.String(32))
    is_confirmed = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    apartments = db.relationship('Apartment', backref='user', lazy='dynamic')
    rents = db.relationship('Rent', backref='user', lazy='dynamic')
    reserves = db.relationship('Reserve', backref='user', lazy='dynamic')

    @classmethod
    def gettter(cls, id):
        return cls.query.filter_by(id=id).first()


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    avatar = db.Column(db.String(32))
    image = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    communities = db.relationship('Community',
        secondary=schools_communities,
        backref=db.backref('schools', lazy='dynamic'),
        lazy='dynamic',
    )


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    add = db.Column(db.Text)
    traffic = db.Column(db.Text)
    pic_map = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    apartments = db.relationship('Apartment', backref='community',
        lazy='dynamic')


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

    title = db.Column(db.String(64), nullable=False)
    subtitle = db.Column(db.String(64))

    num_bedroom = db.Column(db.SmallInteger)
    num_livingroom = db.Column(db.SmallInteger)
    num_bathroom = db.Column(db.SmallInteger)
    price = db.Column(db.Integer)
    area = db.Column(db.Integer)
    type = db.Column(db.SmallInteger)
    pic_contract = db.Column(db.String(32))
    status = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    rooms = db.relationship('Room', backref='apartment', lazy='dynamic')
    comments = db.relationship('Comment', backref='apartment', lazy='dynamic')

    tags = db.relationship('Tag',
        secondary=apartments_tags,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )
    devices = db.relationship('Tag',
        secondary=apartments_devices,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )
    photos = db.relationship('Tag',
        secondary=apartments_photos,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    time_entrance = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    md5 = db.Column(db.String(32), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    dt_start = db.Column(db.DateTime)
    dt_end = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    dt = db.Column(db.DateTime)
    period = db.Column(db.SmallInteger)
    cancelled = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False, index=True)
    from_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.SmallInteger)
    content = db.Column(db.Text)
    unread = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Captcha(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    mobile = db.Column(db.String(11), nullable=False, index=True)
    token = db.Column(db.String(6), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    content = db.Column(db.Text)
    rate = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    type = db.Column(db.String(32), default='public')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    tokens = db.relationship('Token', backref='client', lazy='dynamic')

    @classmethod
    def getter(cls, name):
        return cls.query.filter_by(name=name).first()


class Token(db.Model):
    __table_args__ = (
        db.Index('ix_token_user_id_client_id', 'user_id', 'client_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    access_token = db.Column(db.String(255), unique=True, index=True)
    refresh_token = db.Column(db.String(255), unique=True, index=True)
    token_type = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def getter(cls, access_token=None, refresh_token=None):
        if access_token:
            return cls.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return cls.query.filter_by(refresh_token=refresh_token).first()

    @classmethod
    def setter(cls, token, request, *args, **kwargs):
        token = cls.query.filter_by(
            user_id=request.user.id,
            client_id=request.client.id,
        ).first() or cls(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
        )

        db.session.add(token)
        db.session.commit()
