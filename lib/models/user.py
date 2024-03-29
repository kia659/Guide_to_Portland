from models.__init__ import CURSOR, CONN
from models.helper import Helper
import ipdb

# from models.user_activity import UserActivity


class User(Helper):

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, user_name, id=None):
        self.id = id
        self.user_name = user_name

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        if not isinstance(user_name, str):
            raise TypeError("Username must be a string.")
        elif not 3 <= len(user_name) <= 40:
            raise ValueError("Username must be between 3 and 40 characters long.")
            ipdb.set_trace()
        else:
            self._user_name = user_name

    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()} (
                        id INTEGER PRIMARY KEY,
                        user_name TEXT UNIQUE
                        );
                    """
                )
        except Exception as e:
            return e

    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        INSERT INTO {type(self).pascal_to_camel_plural()}  (user_name)
                        VALUES (?);
                    """,
                    (self.user_name,),
                )
                self.id = CURSOR.lastrowid
        except Exception as e:
            return e

    @classmethod
    def create(cls, user_name):
        new_user = cls(user_name)
        new_user.save()
        return new_user

    def delete(self):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        DELETE FROM {type(self).pascal_to_camel_plural()}
                        WHERE id = ?;
                    """,
                    (self.id,),
                )
                self.id = None
        except Exception as e:
            print(f"Failed to delete due to error: {e}")
            return e

    @classmethod
    def find_by_name(cls, user_name):
        try:
            with CONN:
                sql = f"""
                    SELECT *
                    FROM {cls.pascal_to_camel_plural()}
                    WHERE user_name is ?
                """

            row = CURSOR.execute(sql, (user_name,)).fetchone()
            return cls.instance_from_db(row) if row else None
        except Exception as e:
            return e

    @classmethod
    def instance_from_db(cls, row):
        user = cls.all.get(row[0])
        if user:
            user.user_name = row[1]
        else:
            user = cls(row[1])
            user.id = row[0]
            cls.all[user.id] = user
        return user

    def get_saved_user_activities(self):
        from models.user_activity import UserActivity

        return [
            user_activity
            for user_activity in UserActivity.get_all()
            if user_activity.user_id == self.id
        ]

    def get_saved_activities(self):
        return [
            user_activity.activity()
            for user_activity in self.get_saved_user_activities()
        ]

    def __repr__(self):
        return f"User(id={self.id}, user_name='{self.user_name}')"
