from models.__init__ import CURSOR, CONN
from models.helper import Helper
import ipdb


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
            raise TypeError(
                "Username must be a string."
            )  # Can you input something that's not a string?
        elif not 3 <= len(user_name) <= 40:
            raise ValueError("Username must be between 3 and 40 characters long.")
        elif hasattr(self, "user_name"):
            raise AttributeError("Username cannot be reset.")
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
                    (self.user_name,)
                )
                self.id = CURSOR.lastrowid
        except Exception as e:
            return e

    @classmethod
    def find_by_id(cls, id):
        try:
            CURSOR.execute(
                """
                SELECT * FROM {cls.pascal_to_camel_plural()}
                WHERE id = ?;
                """,
                (id,),
            )
            result = CURSOR.fetchone()
            if result:
                return cls(
                    id=result["id"],
                )
        except Exception as e:
            print(f"Error finding record by id: {e}")
        return None

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

        # instance to view user name in CLI

    def display(self):
        print(f"Username: {self.user_name}")
