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
                contract=file(utils.get_path_from_md5(
                    app.config['UPLOAD_AVATAR_FOLDER'],
                    app.config['DEFAULT_AVATAR_MD5'],
                )), comments=[
                    {'username': 'u1', 'content': 'content1', 'rate': 5},
                    {'username': 'u3', 'content': 'content2', 'rate': 1},
                ], devices=[
                    {'name': 'name1', 'count': 1},
                    {'name': 'name2', 'count': 3},
                    {'name': 'test_for_no_count'},
                    {'name': 'test_for_none_count', 'count': None},
                ], photos=[
                    file(utils.get_path_from_md5(
                        app.config['UPLOAD_AVATAR_FOLDER'],
                        app.config['DEFAULT_AVATAR_MD5'],
                    )),
                    file(utils.get_path_from_md5(
                        app.config['UPLOAD_AVATAR_FOLDER'],
                        app.config['DEFAULT_AVATAR_MD5'],
                    )),
                ], rents=[
                    {'username': 'u4', 'date_start': date(2013, 03, 28),
                        'date_end': date(2014, 04, 01)},
                    {'username': 'u4', 'date_start': date(2013, 04, 28),
                        'date_end': date(2015, 07, 26)},
                ], reserve_choices=[
                    {'date': date(1950, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                    {'date': date(1951, 10, 01), 'time_start': time(12, 34, 56),
                        'time_end': time(12, 56, 34)},
                ], reserves=[
                ], rooms=[
                    {'name': '主卧', 'area': 88, 'price': 8888,
                        'date_entrance': date(1949, 10, 01)},
                    {'name': '次卧1', 'area': 66, 'price': 6666,
                        'date_entrance': date(1950, 10, 01)},
                ], tags=[
                    {'name': '标签1'},
                    {'name': '标签2'},
                    {'name': '标签3'},
                ],
            ),
        ]
        self.apartments[0].reserves = [
            {
                'username': 'u2',
                'choice_id':self.apartments[0].reserve_choice_list[0].id,
            }, {
                'username': 'u2',
                'choice_id':self.apartments[0].reserve_choice_list[1].id,
            },
        ]

def main():
    fake = Fake()

if __name__ == '__main__':
    main()
