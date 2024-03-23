from models.__init__ import CURSOR, CONN

class UserActivity:

    # Dictionary of objects saved to the database.
    all={}
    
    def __init__(self, user_id, activity_id, saved_at, review, rating): # Figure out how the review/ratings will work. Should sit on Activity as well?
        self.user_id = user_id
        self.activity_id = activity_id
        self.saved_at = saved_at
        self.review = review
        self.rating = rating


   # Double check that there should be no properties for: user_id, activity_id, saved_at

    @property
    def review(self):
        return self._review

    @review.setter
    def review(self, review):
        if not isinstance(review, str):
            raise TypeError("Review must be a string.")
        elif not 3 <= len(review) <= 1000:
            raise ValueError("Review must be between 3 and 1000 characters long.")
        else:
            self._review = review

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be a number.")
        elif not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 (lowest) and 5 (Highest).")
        else:
            self._rating = rating

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of User_Activity instances """
        sql = """
            CREATE TABLE IF NOT EXISTS user_activities (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            activity_id INTEGER,
            saved_at DATETIME,
            review TEXT,
            rating INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE Cascade,
            FOREIGN KEY (activity_id) REFERENCES activities(activity_id) ON DELETE Cascade,
            CONSTRAINT unique_activity_per_user UNIQUE(user_id, activity_id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current Employee object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO user_activities (user_id, activity_id, saved_at, review, rating)
                VALUES (?, ?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.user_id, self.activity_id, self.saved_at, self.review, self.rating))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def drop_table(cls):
        """Create a new table to persist the attributes of Review instances"""
        try:
            sql = """
                DROP TABLE IF EXISTS user_activities
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            return e