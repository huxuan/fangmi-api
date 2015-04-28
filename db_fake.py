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
        self.fake_user()
        self.fake_school()
        self.fake_community()
        self.fake_school_community()
        self.fake_apartment()
        self.fake_user_fav_apartment()

    def fake_client(self):
        self.clients = [
            models.Client.setter('fangmi-web'),
            models.Client.setter('fangmi-ios'),
            models.Client.setter('fangmi-android'),
            models.Client.setter('fangmi-test'),
        ]

    def fake_user(self):
        self.users = [
            models.User.create('u1', 'pwd1'),
            models.User.create('u2', 'pwd2'),
            models.User.create('u3', 'pwd2'),
            models.User.create('u4', 'pwd4'),
        ]
        self.user_list = [user.serialize() for user in self.users]

    def fake_school(self):
        self.schools = [
            models.School.create('清华大学', None, None),
            models.School.create('北京大学', None, None),
            models.School.create('人民大学', None, None),
            models.School.create('北京航空航天大学', None, None),
        ]
        self.school_list = [school.serialize() for school in self.schools]

    def fake_community(self):
        self.communities = [
            models.Community.create('小区1', '地址1', '交通1', None),
            models.Community.create('小区2', '地址2', '交通2', None),
            models.Community.create('小区3', '地址3', '交通3', None),
            models.Community.create('小区4', '地址4', '交通4', None),
        ]
        self.community_list = [community.serialize()
            for community in self.communities]

    def fake_school_community(self):
        self.schools[0].communities = self.communities[:]
        self.schools[1].communities = self.communities[1:2]
        self.schools[2].communities = self.communities[:3]
        self.schools[3].communities = self.communities[2:]

    def fake_comments(self):
        pass

    def fake_reserve_choice(self):
        self.reserve_choices = [
        ]

    def fake_apartment(self):
        self.apartments = [
            models.Apartment.create(
                self.users[0].username,
                self.communities[1].id,
                title='title1',
                subtitle='subtitle1',
                address='address1',
                num_bedroom=3,
                num_livingroom=1,
                type=0,
                devices=[
                    {'name': 'name1', 'count': 1},
                    {'name': 'name2', 'count': 3},
                    {'name': 'test_for_no_count'},
                    {'name': 'test_for_none_count', 'count': None},
                ],
                reserve_choices=[
                    {'date': date(1950, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                    {'date': date(1951, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                ],
                rooms=[
                    {'name': '', 'area': 88, 'price': 8888,
                        'date_entrance': date(1949, 10, 01)},
                ],
                tags=[
                    {'name': '标签1'},
                    {'name': '标签2'},
                    {'name': '标签3'},
                ],
            ),
            models.Apartment.create(
                self.users[0].username,
                self.communities[1].id,
                title='title2',
                subtitle='subtitle2',
                address='address2',
                num_bedroom=3,
                num_livingroom=2,
                type=1,
                devices=[
                    {'name': 'name1', 'count': 1},
                    {'name': 'name2', 'count': 3},
                    {'name': 'test_for_no_count'},
                    {'name': 'test_for_none_count', 'count': None},
                ],
                reserve_choices=[
                    {'date': date(1950, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                    {'date': date(1951, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                ],
                rooms=[
                    {'name': '', 'area': 88, 'price': 1111,
                        'date_entrance': date(1949, 10, 01)},
                    {'name': '', 'area': 88, 'price': 2222,
                        'date_entrance': date(1949, 10, 01)},
                    {'name': '', 'area': 88, 'price': 3333,
                        'date_entrance': date(1949, 10, 01)},
                    {'name': '', 'area': 88, 'price': 4444,
                        'date_entrance': date(1949, 10, 01)},
                    {'name': '', 'area': 88, 'price': 5555,
                        'date_entrance': date(1949, 10, 01)},
                ],
                tags=[
                    {'name': '标签1'},
                    {'name': '标签2'},
                    {'name': '标签3'},
                ],
            ),
        ]
        self.apartments[0].photos = [
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
        self.apartments[0].reserves = [
            {
                'username': 'u2',
                'choice_id':self.apartments[0].reserve_choice_list[0].id,
            }, {
                'username': 'u2',
                'choice_id':self.apartments[0].reserve_choice_list[1].id,
            },
        ]
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
        self.apartments[1].reserves = [
            {
                'username': 'u1',
                'choice_id':self.apartments[1].reserve_choice_list[0].id,
            }, {
                'username': 'u3',
                'choice_id':self.apartments[1].reserve_choice_list[1].id,
            },
        ]

    def fake_user_fav_apartment(self):
        self.users[0].append_fav_apartment(self.apartments[0])
        self.users[2].append_fav_apartment(self.apartments[0])


def main():
    fake = Fake()

if __name__ == '__main__':
    main()
