#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_fake.py
Author: huxuan
Email: i(at)huxuan.org
Description: Script to generate fake database.
"""
from datetime import date
from datetime import datetime
from datetime import time

from app import app
from app import models
from app import utils

SCHOOLS = []
COMMUNITIES = []

class Fake(object):

    def __init__(self):
        self.fake_client()
        self.fake_admin()
        self.fake_user()
        self.fake_school()
        self.fake_community()
        self.fake_school_community()
        self.fake_apartment()
        self.fake_apartment_photo()
        self.fake_apartment_rent()
        self.fake_apartment_reserve()
        self.fake_user_fav_apartment()

    def fake_client(self):
        self.clients = [
            models.Client.setter(u'fangmi-web'),
            models.Client.setter(u'fangmi-ios'),
            models.Client.setter(u'fangmi-android'),
            models.Client.setter(u'fangmi-test'),
        ]

    def fake_admin(self):
        models.Admin.create('admin', 'password')

    def fake_user(self):
        self.users = [
            models.User.create(u'u1', u'pwd1'),
            models.User.create(u'u2', u'pwd2'),
            models.User.create(u'u3', u'pwd2'),
            models.User.create(u'u4', u'pwd4'),
        ]
        self.user_list = [user.serialize() for user in self.users]

    def fake_school(self):
        self.schools = [
            models.School.create(u'清华大学', None, None),
            models.School.create(u'北京大学', None, None),
            models.School.create(u'人民大学', None, None),
            models.School.create(u'北京航空航天大学', None, None),
        ]
        self.school_list = [school.serialize() for school in self.schools]

    def fake_community(self):
        self.communities = [
            models.Community.create(u'小区1', u'地址1', u'交通1', None),
            models.Community.create(u'小区2', u'地址2', u'交通2', None),
            models.Community.create(u'小区3', u'地址3', u'交通3', None),
            models.Community.create(u'小区4', u'地址4', u'交通4', None),
        ]
        self.community_list = [community.serialize()
            for community in self.communities]

    def fake_school_community(self):
        self.schools[0].communities = self.communities[:]
        self.schools[1].communities = self.communities[1:2]
        self.schools[2].communities = self.communities[:3]
        self.schools[3].communities = self.communities[2:]

    def fake_apartment(self):
        self.apartments = [
            models.Apartment.create(
                self.users[0].username,
                self.communities[1].id,
                title=u'标题1 而且 要 长',
                subtitle=u'副标题也要长长的才有感觉嘛',
                address=u'地址虽然是小三，但也要浪的长~',
                num_bedroom=3,
                num_livingroom=1,
                type=0,
                devices=[
                    {u'name': u'name1', u'count': 1},
                    {u'name': u'name2', u'count': 3},
                    {u'name': u'test_for_no_count'},
                    {u'name': u'test_for_none_count', u'count': None},
                ],
                reserve_choices=[
                    {u'date': date(1950, 10, 01), u'time_start': time(12, 34, 56),
                        u'time_end': time(12, 56, 34)},
                    {u'date': date(1951, 10, 01), u'time_start': time(12, 34, 56),
                        u'time_end': time(12, 56, 34)},
                ],
                rooms=[
                    {u'name': u'', u'area': 88, u'price': 8888,
                        u'date_entrance': date(1949, 10, 01)},
                ],
                tags=[
                    {u'name': u'标签1'},
                    {u'name': u'标签2'},
                    {u'name': u'标签3'},
                ],
            ),
            models.Apartment.create(
                self.users[0].username,
                self.communities[1].id,
                title=u'我是不二标题',
                subtitle=u'我不是二副标题',
                address=u'我二是地址',
                num_bedroom=3,
                num_livingroom=2,
                type=1,
                devices=[
                    {u'name': u'name1', u'count': 1},
                    {u'name': u'name2', u'count': 3},
                    {u'name': u'test_for_no_count'},
                    {u'name': u'test_for_none_count', u'count': None},
                ],
                reserve_choices=[
                    {u'date': date(1950, 10, 01), u'time_start': time(12, 34, 56),
                        u'time_end': time(12, 56, 34)},
                    {u'date': date(1951, 10, 01), u'time_start': time(12, 34, 56),
                        u'time_end': time(12, 56, 34)},
                ],
                rooms=[
                    {u'name': u'', u'area': 88, u'price': 1111,
                        u'date_entrance': date(1949, 10, 01)},
                    {u'name': u'', u'area': 88, u'price': 2222,
                        u'date_entrance': date(1949, 10, 01)},
                    {u'name': u'', u'area': 88, u'price': 3333,
                        u'date_entrance': date(1949, 10, 01)},
                    {u'name': u'', u'area': 88, u'price': 4444,
                        u'date_entrance': date(1949, 10, 01)},
                    {u'name': u'', u'area': 88, u'price': 5555,
                        u'date_entrance': date(1949, 10, 01)},
                ],
                tags=[
                    {u'name': u'标签1'},
                    {u'name': u'标签2'},
                    {u'name': u'标签3'},
                ],
            ),
        ]

    def fake_apartment_photo(self):
        self.apartments[0].photos = [
            file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            )),
            file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            )),
            file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            )),
        ]
        self.apartments[0].contract = file(
            utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5']
        ))
        self.apartments[1].photos = [
            file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            )),
            file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            )),
        ]
        self.apartments[1].contract = file(
            utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5']
        ))

    def fake_apartment_reserve(self):
        self.reserves = [
            models.Reserve.create(
                self.users[1].username,
                self.apartments[0].reserve_choice_list[0].id,
            ),
            models.Reserve.create(
                self.users[2].username,
                self.apartments[0].reserve_choice_list[1].id,
            ),
            models.Reserve.create(
                self.users[3].username,
                self.apartments[1].reserve_choice_list[0].id,
            ),
            models.Reserve.create(
                self.users[0].username,
                self.apartments[1].reserve_choice_list[1].id,
            ),
        ]

    def fake_apartment_rent(self):
        self.rents = [
            models.Rent.create(
                self.users[0].username, self.apartments[0].room_list[0].id,
                date(2015, 01, 01), date(2016, 01, 01),
            ),
            models.Rent.create(
                self.users[1].username, self.apartments[1].room_list[0].id,
                date(2015, 01, 01), date(2016, 01, 01),
            ),
        ]

    def fake_user_fav_apartment(self):
        self.users[0].append_fav_apartment(self.apartments[0])
        self.users[2].append_fav_apartment(self.apartments[0])


def main():
    fake = Fake()

if __name__ == '__main__':
    main()
