#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: db_drop.py
Author: Francis Chan
Email: f1ancis621@gmail.com
Description: script to drop all tables
"""

print 'Please input "fangmi" to confirm you know what you are doing'
confirm = raw_input()

if confirm == 'fangmi':
    from app import db
    db.drop_all()
