#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
import ipdb
from models.user_activity import UserActivity 
from models.user import User
from models.activity import Activity
from datetime import datetime

UserActivity.drop_table()
User.drop_table()
Activity.drop_table()

User.create_table()
Activity.create_table()
UserActivity.create_table()
user1 = User("steph")
user1.save()
activity1 = Activity("PortlandJapanese Garden", "Large Japanese garden with beautiful Japanese landscaping, tranquil ponds, and a traditional tea house. Nice, serene escape from the city.","Experience","https://japanesegarden.org/","123 S main street , city, stat","Arlington Heights")
activity1.save()
user_activity1 = UserActivity(user1.id, activity1.id, datetime.now(), "review", 5)
user_activity1.save()

ipdb.set_trace()
