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
from datetime import timedelta

from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.declarative import ConcreteBase
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import app
from app import db
from app import utils

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


users_fav_apartments = db.Table('users_fav_apartments',
    db.Column('username', db.String(32), db.ForeignKey('user.username')),
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartment.id')),
)

class User(db.Model):
    # Authentication related.
    username = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Online Profile.
    nickname = db.Column(db.String(64), nullable=False, default=username)
    avatar_md5 = db.Column(db.String(32), default=app.config['DEFAULT_AVATAR_MD5'])
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
    pic_student_md5 = db.Column(db.String(32))
    pic_portal_md5 = db.Column(db.String(32))
    is_confirmed = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    apartment_list = db.relationship('Apartment', backref='user', lazy='dynamic')
    rent_list = db.relationship('Rent', backref='user', lazy='dynamic')
    reserve_list = db.relationship('Reserve', backref='user', lazy='dynamic')
    comment_list = db.relationship('Comment', backref='user', lazy='dynamic')
    token_list = db.relationship('Token', backref='user', lazy='dynamic')

    fav_apartments = db.relationship('Apartment',
        secondary=users_fav_apartments,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic',
    )

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def avatar(self):
        return utils.get_url_from_md5(app.config['UPLOAD_AVATAR_URL'],
            self.avatar_md5)

    @avatar.setter
    def avatar(self, stream):
        self.avatar_md5 = utils.save_file(stream,
            app.config['UPLOAD_AVATAR_FOLDER'])

    @property
    def pic_student(self):
        return utils.get_url_from_md5(app.config['UPLOAD_PIC_STUDENT_URL'],
            self.pic_student_md5)

    @pic_student.setter
    def pic_student(self, stream):
        self.pic_student_md5 = utils.save_file(stream,
            app.config['UPLOAD_PIC_STUDENT_FOLDER'])

    @property
    def pic_portal(self):
        return utils.get_url_from_md5(app.config['UPLOAD_PIC_PORTAL_URL'],
            self.pic_portal_md5)

    @pic_portal.setter
    def pic_portal(self, stream):
        self.pic_portal_md5 = utils.save_file(stream,
            app.config['UPLOAD_PIC_PORTAL_FOLDER'])

    @property
    def num_fav_apartments(self):
        return self.fav_apartments.count()

    @property
    def num_unread_messages(self):
        return Message.query.filter(
            Message.to_username==self.username,
            Message.unread==True,
            Message.deleted==False,
        ).count()

    @classmethod
    def getter(cls, username, password, *args, **kwargs):
        user = cls.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user
        return None

    @classmethod
    def create(cls, username, password):
        user = cls(
            username=username,
            password=password,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get(cls, username, filter_deleted=True, nullable=False):
        res = cls.get_query.filter_by(username=username)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_USER_NOT_FOUND)
        return res

    @classmethod
    def check_not_exist(cls, username):
        if cls.get(username, nullable=True):
            raise utils.APIException(utils.API_CODE_USER_DUPLICATE)
        return True

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def change_password(self, password):
        self.password = password
        db.session.flush()

    def verify_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        else:
            raise utils.APIException(utils.API_CODE_PASSWORD_INVALID)

    def serialize(self):
        res = dict(
            username=self.username,
            nickname=self.nickname,
            avatar=self.avatar,
            status=self.status,
            birthday=utils.convert_date(self.birthday),
            horoscope=self.horoscope,
            gender=self.gender,
            mobile=self.mobile,
            num_fav_apartments=self.num_fav_apartments,
            num_unread_messages=self.num_unread_messages,
            is_confirmed=self.is_confirmed,
            is_student=self.is_student,
            created_at=utils.convert_datetime(self.created_at),
            deleted=self.deleted,
        )
        if self.is_student:
            res.update(dict(
                school=self.school,
                major=self.major,
                student_id=self.student_id,
                pic_student=self.pic_student,
                pic_portal=self.pic_portal,
            ))
        if self.is_confirmed:
            res.update(dict(
                name=self.name,
                id_number=self.id_number,
            ))
        return res


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    avatar_md5 = db.Column(db.String(32))
    image_md5 = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    communities = db.relationship('Community',
        secondary=schools_communities,
        backref=db.backref('schools', lazy='dynamic'),
        lazy='dynamic',
    )

    @property
    def avatar(self):
        return utils.get_url_from_md5(app.config['UPLOAD_SCHOOL_AVATAR_URL'],
            self.avatar_md5)

    @avatar.setter
    def avatar(self, stream):
        self.avatar_md5 = utils.save_file(stream,
            app.config['UPLOAD_SCHOOL_AVATAR_FOLDER'])

    @property
    def image(self):
        return utils.get_url_from_md5(app.config['UPLOAD_SCHOOL_IMAGE_URL'],
            self.image_md5)

    @image.setter
    def image(self, stream):
        self.image_md5 = utils.save_file(stream,
            app.config['UPLOAD_SCHOOL_IMAGE_FOLDER'])

    @classmethod
    def create(cls, name, avatar, image):
        school = cls(
            name=name,
            avatar=avatar,
            image=image,
        )
        db.session.add(school)
        db.session.commit()
        return school

    @classmethod
    def get(cls, name, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(name=name)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_SCHOOL_NOT_FOUND)
        return res

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            avatar=self.avatar,
            image=self.image,
            created_at=utils.convert_datetime(self.created_at),
            deleted=self.deleted,
        )


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    add = db.Column(db.Text)
    traffic = db.Column(db.Text)
    pic_map = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    apartments = db.relationship('Apartment', backref='community',
        lazy='dynamic')

    @classmethod
    def get(cls, id=None, name=None, filter_deleted=True, nullable=False):
        res = cls.query
        if id:
            res = res.filter_by(id=id)
        if name:
            res = res.filter_by(name=name)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_COMMUNITY_NOT_FOUND)
        return res

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('user.username'))
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

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    rooms = db.relationship('Room', backref='apartment', lazy='dynamic')
    comments = db.relationship('Comment', backref='apartment', lazy='dynamic')

    tags = db.relationship('Tag',
        secondary=apartments_tags,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )
    devices = db.relationship('Device',
        secondary=apartments_devices,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )
    photos = db.relationship('Photo',
        secondary=apartments_photos,
        backref=db.backref('apartments', lazy='dynamic'),
        lazy='dynamic',
    )


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    time_entrance = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    md5 = db.Column(db.String(32), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    dt_start = db.Column(db.DateTime)
    dt_end = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    dt = db.Column(db.DateTime)
    period = db.Column(db.SmallInteger)
    cancelled = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Message(db.Model):
    __table_args__ = (
        db.Index('ix_message_to_username_unread_deleted',
            'to_username', 'unread', 'deleted'),
    )

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False, index=True)
    from_username = db.Column(db.String(32), db.ForeignKey('user.username'))
    to_username = db.Column(db.String(32), db.ForeignKey('user.username'))
    type = db.Column(db.SmallInteger)
    content = db.Column(db.Text)
    unread = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Captcha(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    mobile = db.Column(db.String(11), nullable=False, index=True)
    token = db.Column(db.String(6), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def verify(cls, mobile, token):
        return True # NOTE(huxuan): Hack verify() until captcha feature is done.
        captcha = cls.query.filter_by(mobile=mobile).filter_by(deleted=False)\
            .first()
        if not captcha:
            raise utils.APIException(utils.API_CODE_CAPTCHA_NOT_FOUND)
        if captcha.token != token:
            raise utils.APIException(utils.API_CODE_CAPTCHA_INVALID)
        captcha.deleted = True
        db.session.flush()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    content = db.Column(db.Text)
    rate = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)


class Client(db.Model):
    client_id = db.Column(db.String(64), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    tokens = db.relationship('Token', backref='client', lazy='dynamic')

    @property
    def client_type(self):
        return 'public'

    @property
    def default_redirect_uri(self):
        return ''

    @property
    def default_scopes(self):
        return []

    @property
    def allowed_grant_types(self):
        return ['password']

    @classmethod
    def getter(cls, client_id):
        return cls.query.filter_by(client_id=client_id).first()

    @classmethod
    def setter(cls, client_id):
        client = cls.query.filter_by(client_id=client_id).first()
        if not client:
            client = cls(client_id=client_id)
            db.session.add(client)
            db.session.commit()


class Token(db.Model):
    __table_args__ = (
        db.Index('ix_token_username_client_id', 'username', 'client_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    client_id = db.Column(db.String(64), db.ForeignKey('client.client_id'))

    access_token = db.Column(db.String(255), unique=True, index=True)
    refresh_token = db.Column(db.String(255), unique=True, index=True)
    token_type = db.Column(db.String(32))
    expires = db.Column(db.DateTime)

    @property
    def scopes(self):
        return []

    @classmethod
    def getter(cls, access_token=None, refresh_token=None):
        if access_token:
            return cls.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return cls.query.filter_by(refresh_token=refresh_token).first()

    @classmethod
    def setter(cls, token, request, *args, **kwargs):
        tokens = cls.query.filter_by(
            username=request.user.username,
            client_id=request.client.client_id,
        )

        for t in tokens:
            db.session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.now() + timedelta(seconds=expires_in)

        token = cls(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            expires=expires,
            client_id=request.client.client_id,
            username=request.user.username,
        )

        db.session.add(token)
        db.session.commit()
        return token
