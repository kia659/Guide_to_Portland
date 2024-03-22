#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from models.user_activity import User_Activity 
from models.user import User

User_Activity.create_table()
User.create_table()
user1 = User("steph")
user_activity1 = User_Activity(1, 2, saved_at, review, rating)

ipdb.set_trace()
