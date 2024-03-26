from models.__init__ import CONN, CURSOR
from models.user import User
from models.activity import Activity
from models.helper import Helper


class UserActivity(Helper):

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(
        self, user_id, activity_id, saved_at, review, rating
    ):  # Figure out how the review/ratings will work. Should sit on Activity as well?
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
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()} (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        activity_id INTEGER,
                        saved_at DATETIME,
                        review TEXT,
                        rating INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE Cascade,
                        FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE Cascade,
                        CONSTRAINT unique_activity_per_user UNIQUE(user_id, activity_id)
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
                        INSERT INTO {type(self).pascal_to_camel_plural()} 
                        (user_id, activity_id, saved_at, review, rating)
                        VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        self.user_id,
                        self.activity_id,
                        self.saved_at,
                        self.review,
                        self.rating,
                    ),
                )
            self.id = CURSOR.lastrowid
        except Exception as e:
            return e

    def update_rating_and_review(self, new_rating, new_review):
        self.rating = new_rating
        self.review = new_review
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        UPDATE {type(self).pascal_to_camel_plural()} 
                        SET review = ?, rating = ? 
                        WHERE user_id = ? AND activity_id = ?;
                    """,
                    (self.rating, self.review, self.user_id, self.activity_id),
                )
        except Exception as e:
            print(f"Failed to update activity rating and review: {e}")
            return e

    #  NEED TO SEE IF THIS ONLY DELETES ONE ACTIVITY?
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
    def add_activity_to_user(cls, user_id, activity_id):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        INSERT INTO {cls.pascal_to_camel_plural()} 
                        (user_id, activity_id)
                        VALUES (?, ?);
                    """,
                    (
                        user_id,
                        activity_id,
                    ),
                )
            return True
        except Exception as e:
            print(f"Failed to add activity: {e}")
            return e

    @classmethod
    def instance_from_db(cls, row):
        user_activity = cls.all.get(row[0])
        if user_activity:
            user_activity.user_id = row[1]
            user_activity.activity_id = row[2]
            user_activity.saved_at = row[3]
            user_activity.review = row[4]
            user_activity.rating = row[5]
        else:
            user_activity = cls(row[1], row[2], row[3], row[4], row[5], id=row[0])
            cls.all[user_activity.id] = user_activity
        return user_activity
