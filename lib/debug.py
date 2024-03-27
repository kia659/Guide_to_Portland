#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.user_activity import UserActivity
from models.user import User
from models.activity import Activity
from datetime import datetime
from models.helper import Helper

# Helper.drop_table()
# UserActivity.drop_table()
# User.drop_table()
# Activity.drop_table()

# User.create_table()
# Activity.create_table()
# UserActivity.create_table()
user1 = User("steph")
User.get_saved_user_activities()
# user1.save()
# activity1 = Activity(
#     "Test Debug Experience",
#     "Description for experience.",
#     "Free Experiences",
#     "123 S main street, Portland, OR 97205",
#     "Arlington Heights",
#     "https://www.test.com",
# )
# activity1.save()
# user_activity1 = UserActivity(user1.id, activity1.id, datetime.now(), "review", 5)
# user_activity1.save()
if __name__ == "__main__":
    import ipdb

    ipdb.set_trace()
