from __init__ import CURSOR, CONN

class User:
    
    def __init__(self, user_name, user_id=None): 
        self.user_id = user_id
        self.user_name = user_name
        
    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        if not isinstance(user_name, str):
            raise TypeError("Username must be a string.") # Can you input something that's not a string? 
        elif not 3 <= len(user_name) <= 40:
            raise ValueError("Username must be between 3 and 40 characters long.")
        elif hasattr(self, "user_name"):
            raise AttributeError("Username cannot be reset.")
        else:
            self._user_name = user_name

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of User_Activity instances """
        sql = """
            CREATE TABLE IF NOT EXISTS user_activities (
            user_id INTEGER PRIMARY KEY UNIQUE,
            user_name TEXT UNIQUE
            )
        """
        CURSOR.execute(sql)
        CONN.commit()