#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_fake.py
Author: huxuan
Email: i(at)huxuan.org
Description: Script to generate fake database.
"""
from app import app
from app import models

def fake_client():
    models.Client.setter('fangmi-web')

def fake_user():
    models.User.create('u1', 'pwd1')
    models.User.create('u2', 'pwd2')

def main():
    fake_client()
    fake_user()

if __name__ == '__main__':
    main()
