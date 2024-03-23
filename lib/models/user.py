from models.__init__ import CURSOR, CONN

class User:
    
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
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_name TEXT UNIQUE
                )
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            return e

    def save(self):
        """ Insert a new row with user_name of the current User object."""
        sql = """
                INSERT INTO users (user_name)
                VALUES (?)
        """

        CURSOR.execute(sql, (self.user_name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists User instances """
        try:
            sql = """
                DROP TABLE IF EXISTS users
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            return e