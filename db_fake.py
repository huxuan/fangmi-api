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
from app import db
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
        self.real_user()
        db.session.commit()

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
            # models.User.create(u'u1', u'pwd1'),
            # models.User.create(u'u2', u'pwd2'),
            # models.User.create(u'u3', u'pwd2'),
            # models.User.create(u'u4', u'pwd4'),
            models.User.create(u'18525325318', u'1qaz2wsxE'),
            models.User.create(u'17701260830', u'123456'),
            models.User.create(u'13693555092', u'123456'),
            models.User.create(u'18525325316', u'123456'),
        ]
        for user in self.users:
            user.pic_student = file(utils.get_path_from_md5(
                app.config['UPLOAD_AVATAR_FOLDER'],
                app.config['DEFAULT_AVATAR_MD5'],
            ))
        self.user_list = [user.serialize() for user in self.users]

    def real_user(self):
        fangmi_msg_user = models.User.create(u'房蜜提醒', u'FunMiNotify')
        fangmi_msg_user.avatar = file(utils.get_path_from_md5(
            app.config['UPLOAD_AVATAR_FOLDER'],
            'a687d3bbae64f8183cbf213ab1e1eda7',
        ))

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
            models.Community.create(u'清华东路27号院', u'北京市海淀区五道口', u'交通1',u'1001093',u'116.358129,40.006816', None),
            models.Community.create(u'清华园', u'北京市海淀区五道口', u'交通2',u'1003033',u'116.335077,39.999936', None),
            models.Community.create(u'清华大学西北小区', u'北京市海淀区五道口', u'交通3',u'1005397',u'116.321606,40.006858', None),
            models.Community.create(u'北航家属院', u'北京市海淀区知春路', u'交通4',u'1002113',u'116.362597,40.00491', None),
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
                self.communities[0].id,
                title=u'清华东路27号院2室一厅',
                subtitle=u'挥泪转租低价好房,整租',
                address=u'北京市海淀区五道口',
                num_bedroom=3,
                num_livingroom=1,
                type=0,
                devices=[
                    {u'name': u'chuang', u'count': 1},
                    {u'name': u'weishengjian', u'count': 3},
                    {u'name': u'dianshiji'},
                    {u'name': u'chufang', u'count': None},
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
                    {u'name': u'整租低价'},
                    {u'name': u'位置优越'},
                    {u'name': u'周边便捷'},
                ],
            ),
            models.Apartment.create(
                self.users[0].username,
                self.communities[3].id,
                title=u'北航家属院两室一厅',
                subtitle=u'挥泪转租低价好房,合租',
                address=u'北京市海淀区知春路',
                num_bedroom=3,
                num_livingroom=2,
                type=1,
                devices=[
                    {u'name': u'xiyiji', u'count': 1},
                    {u'name': u'wifi', u'count': 3},
                    {u'name': u'chuang'},
                    {u'name': u'kongtiao', u'count': None},
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
                    {u'name': u'舍友好'},
                    {u'name': u'近北航'},
                    {u'name': u'交通便利'},
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
