#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_drop.py
Author: huxuan
Email: i(at)huxuan.org
Description: Script to drop all tables
"""

print 'Please input "fangmi" to confirm you know what you are doing'
confirm = raw_input()

if confirm == 'fangmi':
    from app import db
    db.drop_all()
