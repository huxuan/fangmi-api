#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: models.py
Author: huxuan
Email: i(at)huxuan.org
Description: Models for FangMi API.
"""
import sys
sys.path.insert(0, 'Flask-WhooshAlchemy')
import flask_whooshalchemy as whooshalchemy

from datetime import date
from datetime import datetime
from datetime import timedelta
import operator
import random

from sqlalchemy import and_
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.declarative import ConcreteBase
from werkzeug import datastructures
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import app
from app import db
from app import utils


schools_communities = db.Table('schools_communities',
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id')),
)


apartments_tags = db.Table('apartments_tags',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartments.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
)


users_fav_apartments = db.Table('users_fav_apartments',
    db.Column('username', db.String(32), db.ForeignKey('users.username')),
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartments.id')),
)


class User(db.Model):
    __tablename__ = 'users'

    # Authentication related.
    username = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Online Profile.
    nickname = db.Column(db.String(64), nullable=False, default=username)
    avatar_md5 = db.Column(db.String(32),
        default=app.config['DEFAULT_AVATAR_MD5'])
    status = db.Column(db.Text)
    birthday = db.Column(db.Date)
    horoscope = db.Column(db.SmallInteger)
    gender = db.Column(db.Boolean)

    # Personal Information.
    real_name = db.Column(db.String(16))
    mobile = db.Column(db.String(11), default=username)
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

    apartment_list = db.relationship('Apartment', backref='user',
        lazy='dynamic')
    rent_list = db.relationship('Rent', backref='user', lazy='dynamic')
    reserve_list = db.relationship('Reserve', backref='user', lazy='dynamic')
    comment_list = db.relationship('Comment', backref='user', lazy='dynamic')
    token_list = db.relationship('Token', backref='user', lazy='dynamic')

    fav_apartment_list = db.relationship('Apartment',
        secondary=users_fav_apartments,
        backref=db.backref('fav_users', lazy='dynamic'),
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
        return self.fav_apartment_list.count()

    @property
    def num_unread_messages(self):
        return Message.query.filter_by(
            to_username=self.username,
            unread=True,
            deleted=False,
        ).count()

    @property
    def fav_apartments(self):
        return [apartment.serialize() for apartment in self.fav_apartment_list]

    @fav_apartments.setter
    def fav_apartments(self, fav_apartments):
        self.fav_apartment_list = fav_apartments

    @property
    def birthday_info(self):
        return self.birthday and self.birthday.isoformat()

    @classmethod
    def getter(cls, username, password, *args, **kwargs):
        user = cls.get(username)
        if user.verify_password(password):
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
        res = cls.query.filter_by(username=username)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_USER_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, filter_deleted=True, limit=10):
        res = cls.query
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.limit(limit)
        return res.all()

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

    def append_fav_apartment(self, apartment):
        if not self.is_fav_apartment(apartment.id):
            self.fav_apartment_list.append(apartment)
        db.session.commit()

    def remove_fav_apartment(self, apartment):
        if self.is_fav_apartment(apartment.id):
            self.fav_apartment_list.remove(apartment)
        db.session.commit()

    def fav_apartment_action(self, apartment_id, action):
        apartment = Apartment.get(apartment_id)
        if action == 'append':
            self.append_fav_apartment(apartment)
        elif action == 'remove':
            self.remove_fav_apartment(apartment)

    def is_fav_apartment(self, apartment_id):
        return self.fav_apartment_list.filter(
            users_fav_apartments.c.apartment_id == apartment_id).count() > 0

    def get_num_unread_from_username(self, from_username):
        return Message.query.filter_by(
            from_username=from_username,
            to_username=self.username,
            unread=True,
            deleted=False,
        ).count()

    def get_conversion(self):
        conversation_list = {}
        for to_username, max_id in Message.query.with_entities(
                Message.to_username,
                db.func.max(Message.id)
            ).filter_by(from_username=self.username
            ).group_by(Message.to_username).all():
            conversation_list[to_username] = max(
                conversation_list.get(to_username, 0), max_id)
        for from_username, max_id in Message.query.with_entities(
                Message.from_username,
                db.func.max(Message.id)
            ).filter_by(to_username=self.username
            ).group_by(Message.from_username).all():
            conversation_list[from_username] = max(
                conversation_list.get(from_username, 0), max_id)
        conversation_list = sorted(conversation_list.items(),
            key=operator.itemgetter(1), reverse=True)
        return [{
            'user': User.get(username).serialize(),
            'message': Message.get(message_id).serialize(),
            'num_unread': self.get_num_unread_from_username(username),
        } for username, message_id in conversation_list]


    def serialize(self):
        res = dict(
            username=self.username,
            nickname=self.nickname,
            avatar=self.avatar,
            status=self.status,
            birthday=self.birthday_info,
            horoscope=self.horoscope,
            gender=self.gender,
            mobile=self.mobile,
            num_fav_apartments=self.num_fav_apartments,
            num_unread_messages=self.num_unread_messages,
            is_confirmed=self.is_confirmed,
            is_student=self.is_student,
            #fav_apartments=self.fav_apartments,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
            # Student related information.
            school=self.school,
            major=self.major,
            student_id=self.student_id,
            pic_student=self.pic_student,
            pic_portal=self.pic_portal,
            # Real name confirm information.
            real_name=self.real_name,
            id_number=self.id_number,
        )
        return res


class School(db.Model):
    __tablename__ = 'schools'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    avatar_md5 = db.Column(db.String(32))
    image_md5 = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    community_list = db.relationship('Community',
        secondary=schools_communities,
        backref=db.backref('school_list', lazy='dynamic'),
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

    @property
    def communities(self):
        return [community.serialize() for community in self.community_list]

    @communities.setter
    def communities(self, communities):
        self.community_list = communities
        db.session.commit()

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
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_SCHOOL_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, filter_deleted=True):
        res = cls.query
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    @classmethod
    def search(cls, q, filter_deleted=True):
        res = cls.query.whoosh_search(q)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def append_community(self, community):
        if not self.has_community(community.id):
            self.community_list.append(community)
        db.session.commit()

    def remove_community(self, community):
        if self.has_community(community.id):
            self.community_list.remove(community)
        db.session.commit()

    def community_action(self, community_id, action):
        community = Community.get(community_id)
        if action == 'append':
            self.append_community(community)
        elif action == 'remove':
            self.remove_community(community)

    def has_community(self, community_id):
        return self.community_list.filter(
            schools_communities.c.community_id == community_id).count() > 0

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            avatar=self.avatar,
            image=self.image,
            #communities=self.communities,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Community(db.Model):
    __tablename__ = 'communities'
    __searchable__ = ['name', 'address', 'traffic']

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    address = db.Column(db.String(255))
    traffic = db.Column(db.String(255))
    map_md5 = db.Column(db.String(32))

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    apartment_list = db.relationship('Apartment', backref='community',
        lazy='dynamic')

    @property
    def map(self):
        return utils.get_url_from_md5(app.config['UPLOAD_COMMUNITY_MAP_URL'],
            self.map_md5)

    @map.setter
    def map(self, stream):
        self.map_md5 = utils.save_file(stream,
            app.config['UPLOAD_COMMUNITY_MAP_FOLDER'])

    @property
    def schools(self):
        return [school.serialize() for school in self.school_list]

    @schools.setter
    def schools(self, schools):
        self.school_list = schools
        db.session.commit()

    @property
    def apartments(self):
        return [apartment.serialize() for apartment in self.apartment_list]

    @classmethod
    def create(cls, name, address, traffic, map):
        community = cls(
            name=name,
            address=address,
            traffic=traffic,
            map=map,
        )
        db.session.add(community)
        db.session.commit()
        return community

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_NOT_FOUND,
                name=cls.__tablename__)
        return res

    @classmethod
    def gets(cls, filter_deleted=True):
        res = cls.query
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    @classmethod
    def search(cls, q, filter_deleted=True):
        res = cls.query.whoosh_search(q)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def append_school(self, school):
        if not self.has_school(school.id):
            self.school_list.append(school)
        db.session.commit()

    def remove_school(self, school):
        if self.has_school(school.id):
            self.school_list.remove(school)
        db.session.commit()

    def school_action(self, school_id, action):
        school = School.get(school_id)
        if action == 'append':
            self.append_school(school)
        elif action == 'remove':
            self.remove_school(school)

    def has_school(self, school_id):
        return self.school_list.filter(
            schools_communities.c.school_id == school_id).count() > 0

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            address=self.address,
            traffic=self.traffic,
            map=self.map,
            schools=self.schools,
            #apartments=self.apartments,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Apartment(db.Model):
    __tablename__ = 'apartments'
    __searchable__ = ['title', 'subtitle', 'address']

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))

    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(64))
    address = db.Column(db.String(64))
    contract_md5 = db.Column(db.String(32))
    num_bathroom = db.Column(db.SmallInteger)
    num_bedroom = db.Column(db.SmallInteger)
    num_livingroom = db.Column(db.SmallInteger)
    type = db.Column(db.SmallInteger)
    cancelled = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    comment_list = db.relationship('Comment', backref='apartment',
        lazy='dynamic')
    device_list = db.relationship('Device', backref='apartment', lazy='dynamic')
    photo_list = db.relationship('Photo', backref='apartment', lazy='dynamic')
    rent_list = db.relationship('Rent', backref='apartment', lazy='dynamic')
    reserve_list = db.relationship('Reserve', backref='apartment',
        lazy='dynamic')
    reserve_choice_list = db.relationship('ReserveChoice', backref='apartment',
        lazy='dynamic')
    room_list = db.relationship('Room', backref='apartment', lazy='dynamic')

    tag_list = db.relationship('Tag',
        secondary=apartments_tags,
        backref=db.backref('apartment_list', lazy='dynamic'),
        lazy='dynamic',
    )

    @property
    def user_info(self):
        return self.user.serialize()

    @user_info.setter
    def user_info(self, user):
        self.username = user.username

    @property
    def community_info(self):
        return self.community.serialize()

    @community_info.setter
    def community_info(self, community):
        self.community_id = community.id

    @property
    def contract(self):
        return utils.get_url_from_md5(app.config['UPLOAD_CONTRACT_URL'],
            self.contract_md5)

    @contract.setter
    def contract(self, stream):
        self.contract_md5 = utils.save_file(stream,
            app.config['UPLOAD_CONTRACT_FOLDER'])

    @property
    def comments(self):
        return [comment.serialize() for comment in self.comment_list]

    @comments.setter
    def comments(self, comments):
        self.comment_list = [
            Comment.create(
                comment['username'],
                self.id,
                comment['content'],
                comment['rate'],
            ) for comment in comments]
        db.session.commit()

    @property
    def devices(self):
        return [device.serialize() for device in self.device_list]

    @devices.setter
    def devices(self, devices):
        self.device_list = [
            Device.create(
                self.id,
                device['name'],
                device.get('count', None),
            ) for device in devices]
        db.session.commit()

    @property
    def photos(self):
        return [photo.serialize() for photo in self.photo_list]

    @photos.setter
    def photos(self, photos):
        self.photo_list = [
            Photo.create(
                self.id,
                photo,
            ) for photo in photos]
        db.session.commit()

    @property
    def reserve_choices(self):
        return [reserve_choice.serialize()
            for reserve_choice in self.reserve_choice_list]

    @reserve_choices.setter
    def reserve_choices(self, reserve_choices):
        self.reserve_choice_list = [
            ReserveChoice.create(
                self.id,
                reserve_choice['date'],
                reserve_choice['time_start'],
                reserve_choice['time_end'],
            ) for reserve_choice in reserve_choices]
        db.session.commit()

    @property
    def rooms(self):
        return [room.serialize() for room in self.room_list]

    @rooms.setter
    def rooms(self, rooms):
        self.room_list = [
            Room.create(
                self.id,
                room['name'],
                room['area'],
                room['price'],
                room['date_entrance'],
            ) for room in rooms]
        db.session.commit()

    @property
    def tags(self):
        return [tag.serialize() for tag in self.tag_list]

    @tags.setter
    def tags(self, tags):
        self.tag_list = [
            Tag.create(
                tag['name'],
            ) for tag in tags]
        db.session.commit()

    @property
    def num_fav_users(self):
        return self.fav_users.count()

    @property
    def num_reserve(self):
        return self.reserve_list.count()

    @property
    def min_price(self):
        return min([room.price for room in self.room_list])

    @property
    def max_price(self):
        return max([room.price for room in self.room_list])

    @property
    def status(self):
        for room in self.room_list:
            if room.status:
                return True
        return False

    @classmethod
    def create(cls, username, community_id, title="", subtitle="", address="",
        num_bathroom=0, num_bedroom=0, num_livingroom=0, type=0, devices=[],
        reserve_choices=[], rooms=[], tags=[]):
        apartment = cls(
            username=username,
            community_id=community_id,
            title=title,
            subtitle=subtitle,
            address=address,
            num_bathroom=num_bathroom,
            num_bedroom=num_bedroom,
            num_livingroom=num_livingroom,
            type=type,
            devices=devices,
            reserve_choices=reserve_choices,
            rooms=rooms,
            tags=tags,
        )
        db.session.add(apartment)
        db.session.commit()
        return apartment

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_APARTMENT_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, username=None, community_id=None, school_id=None,
        q=None, filter_cancelled=True, filter_deleted=True, limit=10):
        res = cls.query
        if username:
            res = res.filter_by(username=username)
        if community_id:
            res = res.filter_by(community_id=community_id)
        if school_id:
            school = School.get(school_id)
            community_ids = [community.id
                for community in school.community_list]
            res = res.filter(Apartment.community_id.in_(community_ids))
        if filter_cancelled:
            res = res.filter_by(cancelled=False)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.limit(limit).all()
        return res

    @classmethod
    def search(cls, q, filter_deleted=True):
        res = cls.query.whoosh_search(q)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def verify_owner(self, username):
        if self.username != username:
            raise utils.APIException(utils.API_CODE_NOT_AUTHORIZED,
                name=self.__tablename__)
        return True

    def serialize(self, oauth_user=None):
        res = dict(
            id=self.id,
            user=self.user_info,
            community=self.community_info,
            title=self.title,
            subtitle=self.subtitle,
            address=self.address,
            contract=self.contract,
            num_bathroom=self.num_bathroom,
            num_bedroom=self.num_bedroom,
            num_livingroom=self.num_livingroom,
            num_fav_users=self.num_fav_users,
            num_reserve=self.num_reserve,
            min_price=self.min_price,
            max_price=self.max_price,
            status=self.status,
            cancelled=self.cancelled,
            type=self.type,
            comments=self.comments,
            devices=self.devices,
            photos=self.photos,
            reserve_choices=self.reserve_choices,
            rooms=self.rooms,
            tags=self.tags,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )
        if oauth_user:
            res.update(dict(
                is_favorited=oauth_user.is_fav_apartment(self.id),
            ))
        return res


class ReserveChoice(db.Model):
    __tablename__ = 'reserve_choices'

    id = db.Column(db.Integer, primary_key=True)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    date = db.Column(db.Date)
    time_start = db.Column(db.Time)
    time_end = db.Column(db.Time)

    reserves = db.relationship('Reserve', backref='reserve_choice',
        lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @classmethod
    def create(cls, apartment_id, date, time_start, time_end):
        reserve_choice = cls(
            apartment_id=apartment_id,
            date=date,
            time_start=time_start,
            time_end=time_end,
        )
        db.session.add(reserve_choice)
        db.session.commit()
        return reserve_choice

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_NOT_FOUND,
                name=cls.__tablename__)
        return res

    @classmethod
    def gets(cls, apartment_id, filter_deleted=True):
        res = cls.query.filter_by(apartment_id=apartment_id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.all()
        return res

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            #apartment=self.apartment_info,
            date=self.date.isoformat(),
            time_start=self.time_start.isoformat(),
            time_end=self.time_end.isoformat(),
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    area = db.Column(db.Integer)
    name = db.Column(db.String(16), nullable=False)
    price = db.Column(db.Integer)
    date_entrance = db.Column(db.Date)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    rent_list = db.relationship('Rent', backref='room', lazy='dynamic')

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @property
    def status(self):
        for rent in self.rent_list:
            if rent.date_start <= date.today() and date.today() < rent.date_end:
                return False
        return True

    @classmethod
    def create(cls, apartment_id, name, area, price, date_entrance):
        room = cls(
            apartment_id=apartment_id,
            name=name,
            area=area,
            price=price,
            date_entrance=date_entrance,
        )
        db.session.add(room)
        db.session.commit()
        return room

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_NOT_FOUND,
                name=cls.__tablename__)
        return res

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            #apartment=self.apartment_info,
            area=self.area,
            name=self.name,
            price=self.price,
            status=self.status,
            date_entrance=self.date_entrance.isoformat(),
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    name = db.Column(db.String(64), nullable=False, index=True)
    count = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @classmethod
    def create(cls, apartment_id, name, count):
        room = cls(
            apartment_id=apartment_id,
            name=name,
            count=count,
        )
        db.session.add(room)
        db.session.commit()
        return room

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            #apartment=self.apartment_info,
            name=self.name,
            count=self.count,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)

    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    photo_md5 = db.Column(db.String(32), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @property
    def photo(self):
        return utils.get_url_from_md5(app.config['UPLOAD_PHOTO_URL'],
            self.photo_md5)

    @photo.setter
    def photo(self, stream):
        self.photo_md5 = utils.save_file(stream,
            app.config['UPLOAD_PHOTO_FOLDER'])

    @classmethod
    def create(cls, apartment_id, photo):
        photo = cls(
            apartment_id=apartment_id,
            photo=photo,
        )
        db.session.add(photo)
        db.session.commit()
        return photo

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            #apartment=self.apartment_info,
            photo=self.photo,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def apartments(self):
        return [apartment.serialize() for apartment in self.apartment_list]

    @classmethod
    def get(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def create(cls, name):
        tag = cls.get(name)
        if not tag:
            tag = cls(
                name=name,
            )
            db.session.add(tag)
            db.session.commit()
        return tag

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            #apartments=self.apartments,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Rent(db.Model):
    __tablename__ = 'rents'
    __table_args__ = (
        db.Index('ix_rent_username_apartment_id', 'username', 'apartment_id'),
        db.Index('ix_rent_username_apartment_id_deleted', 'username',
            'apartment_id', 'deleted'),
        db.Index('ix_rent_apartment_id_deleted', 'apartment_id', 'deleted'),
        db.Index('ix_rent_username_deleted', 'username', 'deleted'),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def user_info(self):
        return self.user.serialize()

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @property
    def room_info(self):
        return self.room.serialize()

    @classmethod
    def create(cls, username, room_id, date_start, date_end, **kwargs):
        room = Room.get(room_id)
        rent = cls(
            username=username,
            apartment_id=room.apartment_id,
            room_id = room_id,
            date_start=date_start,
            date_end=date_end,
        )
        db.session.add(rent)
        db.session.commit()
        return rent

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_RENT_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, username=None, apartment_id=None, filter_deleted=True):
        res = cls.query
        if username:
            res = res.filter_by(username=username)
        if apartment_id:
            res = res.filter_by(apartment_id=apartment_id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def verify_owner(self, username):
        if self.username != username and self.apartment.username != username:
            raise utils.APIException(utils.API_CODE_NOT_AUTHORIZED,
                name=self.__tablename__)

    def serialize(self):
        return dict(
            id=self.id,
            user=self.user_info,
            apartment=self.apartment_info,
            room=self.room_info,
            date_start=self.date_start.isoformat(),
            date_end=self.date_end.isoformat(),
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Reserve(db.Model):
    __tablename__ = 'reserves'
    __table_args__ = (
        db.Index('ix_reserve_username_deleted', 'username', 'deleted'),
        db.Index('ix_reserve_username_apartment_id', 'username',
            'apartment_id'),
        db.Index('ix_reserve_username_apartment_id_deleted', 'username',
            'apartment_id', 'deleted'),
        db.Index('ix_reserve_apartment_id_deleted', 'apartment_id',
            'deleted'),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    reserve_choice_id = db.Column(db.Integer,
        db.ForeignKey('reserve_choices.id'))

    cancelled = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def user_info(self):
        return self.user.serialize()

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @property
    def reserve_choice_info(self):
        return self.reserve_choice.serialize()

    @classmethod
    def create(cls, username, reserve_choice_id):
        reserve_choice = ReserveChoice.get(reserve_choice_id)
        reserve = cls(
            username=username,
            apartment_id=reserve_choice.apartment_id,
            reserve_choice_id=reserve_choice_id,
        )
        db.session.add(reserve)
        db.session.commit()
        return reserve

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_RESERVE_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, username=None, apartment_id=None, filter_deleted=True):
        res = cls.query
        if username:
            res = res.filter_by(username=username)
        if apartment_id:
            res = res.filter_by(apartment_id=apartment_id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.all()
        return res

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def verify_owner(self, username):
        if self.username != username and \
            self.reserve_choice.apartment.username != username:
            raise utils.APIException(utils.API_CODE_NOT_AUTHORIZED,
                name=self.__tablename__)
        return True

    def serialize(self):
        return dict(
            id=self.id,
            user=self.user_info,
            apartment=self.apartment_info,
            reserve_choice=self.reserve_choice_info,
            cancelled=self.cancelled,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = (
        db.Index('ix_message_key_deleted', 'key', 'deleted'),
        db.Index('ix_message_key_to_username_unread', 'key', 'to_username',
            'unread'),
        db.Index('ix_message_key_to_username_unread_deleted', 'key',
            'to_username', 'unread', 'deleted'),
        db.Index('ix_message_from_username_to_username_unread_deleted',
            'from_username', 'to_username', 'unread', 'deleted'),
        db.Index('ix_message_to_username_unread_deleted', 'to_username',
            'unread', 'deleted'),
    )

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False, index=True)
    from_username = db.Column(db.String(32), db.ForeignKey('users.username'))
    to_username = db.Column(db.String(32), db.ForeignKey('users.username'))

    type = db.Column(db.SmallInteger)
    content = db.Column(db.Text)
    unread = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def from_user(self):
        return User.get(self.from_username).serialize()

    @property
    def to_user(self):
        return User.get(self.to_username).serialize()

    @property
    def content_info(self):
        if self.type == 1:
            return self.content
        elif self.type == 2:
            return utils.get_url_from_md5(
                app.config['UPLOAD_MESSAGE_URL'], self.content)

    @content_info.setter
    def content_info(self, content):
        if self.type == 1:
            self.content = content
        elif self.type == 2:
            self.content = utils.save_file(content,
                app.config['UPLOAD_MESSAGE_FOLDER'])

    @classmethod
    def mark_as_read(cls, messages, username):
        for message in messages:
            if message.to_username == username:
                message.unread=False
        db.session.flush()

    @classmethod
    def get_key(cls, from_username, to_username):
        return '_'.join(sorted([from_username, to_username]))

    @classmethod
    def create(cls, from_username, to_username, type, content):
        message = cls(
            key=cls.get_key(from_username, to_username),
            from_username=from_username,
            to_username=to_username,
            type=type,
        )
        message.content_info = content
        db.session.add(message)
        db.session.commit()
        return message

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_MESSAGE_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, to_username, from_username, filter_unread=True,
        filter_deleted=True, **kwargs):
        key=cls.get_key(to_username, from_username)
        res = cls.query.filter_by(key=key)
        if filter_unread:
            res = res.filter(and_(
                Message.to_username == to_username,
                Message.unread == True,
            ))
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.limit(100).all()
        cls.mark_as_read(res, to_username)
        return res

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def verify_owner(self, username):
        if self.from_username != username and self.to_username != username:
            raise utils.APIException(utils.API_CODE_NOT_AUTHORIZED,
                name=self.__tablename__)

    def serialize(self):
        return dict(
            id=self.id,
            from_username=self.from_username,
            to_username=self.to_username,
            content=self.content_info,
            type=self.type,
            unread=self.unread,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))

    content = db.Column(db.Text)
    rate = db.Column(db.SmallInteger)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def user_info(self):
        return self.user.serialize()

    @property
    def apartment_info(self):
        return self.apartment.serialize()

    @classmethod
    def create(cls, username, apartment_id, content, rate):
        rent = cls(
            username=username,
            apartment_id=apartment_id,
            content=content,
            rate=rate,
        )
        db.session.add(rent)
        db.session.commit()
        return rent

    @classmethod
    def get(cls, id, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(id=id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_RENT_NOT_FOUND)
        return res

    @classmethod
    def gets(cls, username=None, apartment_id=None, filter_deleted=True):
        res = cls.query
        if username:
            res = res.filter_by(username=username)
        if apartment_id:
            res = res.filter_by(apartment_id=apartment_id)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        return res.all()

    def set(self, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])
        db.session.flush()

    def serialize(self):
        return dict(
            id=self.id,
            user=self.user_info,
            #apartment=self.apartment_info,
            content=self.content,
            rate=self.rate,
            created_at=self.created_at.isoformat(),
            deleted=self.deleted,
        )


class Captcha(db.Model):
    __tablename__ = 'captchas'

    id = db.Column(db.Integer, primary_key=True)

    mobile = db.Column(db.String(11), unique=True, nullable=False, index=True)
    token = db.Column(db.String(6), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def verify(cls, mobile, token):
        captcha = cls.query.filter_by(mobile=mobile).filter_by(deleted=False)\
            .first()
        if not captcha:
            raise utils.APIException(utils.API_CODE_NOT_FOUND,
                name=cls.__tablename__)
        if captcha.token != token:
            raise utils.APIException(utils.API_CODE_INVALID,
                name=cls.__tablename__)
        captcha.deleted = True
        db.session.flush()
        return True

    @classmethod
    def get(cls, mobile):
        return cls.query.filter_by(mobile=mobile).first()

    @classmethod
    def create(cls, mobile):
        utils.verify_mobile(mobile)
        token = random.randint(100000, 999999)
        captcha = cls.get(mobile)
        if captcha:
            if not captcha.deleted and datetime.now() - captcha.created_at < \
                timedelta(seconds=app.config['EMY_TIMEDELTA_SECONDS']):
                raise utils.APIException(utils.API_CODE_CAPTCHA_EXCEED_FREQUENCY)
            captcha.token = token
            captcha.delted = False
            captcha.created_at = datetime.now()
        else:
            captcha = cls(
                mobile=mobile,
                token=token,
            )
            db.session.add(captcha)
        utils.send_captcha_sms(mobile, token)
        db.session.commit()
        return captcha


class Client(db.Model):
    __tablename__ = 'clients'

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
    __tablename__ = 'tokens'
    __table_args__ = (
        db.Index('ix_token_username_client_id', 'username', 'client_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), db.ForeignKey('users.username'))
    client_id = db.Column(db.String(64), db.ForeignKey('clients.client_id'))

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


class Admin(db.Model):
    __tablename__ = 'admins'

    username = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def create(cls, username, password):
        admin_user = cls(
            username=username,
            password=password,
        )
        db.session.add(admin_user)
        db.session.commit()
        return admin_user

    @classmethod
    def get(cls, username, filter_deleted=True, nullable=False):
        res = cls.query.filter_by(username=username)
        if filter_deleted:
            res = res.filter_by(deleted=False)
        res = res.first()
        if not nullable and not res:
            raise utils.APIException(utils.API_CODE_NOT_FOUND,
                name=cls.__tablename__)
        return res

    def verify_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        else:
            raise utils.APIException(utils.API_CODE_PASSWORD_INVALID)


whooshalchemy.whoosh_index(app, School)
whooshalchemy.whoosh_index(app, Community)
whooshalchemy.whoosh_index(app, Apartment)
