from models.__init__ import CONN, CURSOR
from models.helper import Helper


class Activity(Helper):

    all = {}

    acceptable_activity_types = {
        "Free Experiences",
        "Food Carts",
        "Breweries & Bars",
        "Shops",
        "Paid Experiences",
        "Restaurants",
    }

    def __init__(
        self,
        name,
        description,
        activity_type,
        address,
        neighborhood,
        website=None,
        id=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.address = address
        self.neighborhood = neighborhood
        self.website = website

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("names must be strings")
        elif not value:
            raise AttributeError("names must be string with at least one character")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("descriptions must be strings")
        elif not value:
            raise AttributeError(
                "descriptions must be strings with at least one character"
            )
        self._description = value

    @property
    def activity_type(self):
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        if activity_type not in self.acceptable_activity_types:
            raise ValueError(
                "Invalid activity type. Please choose from: {}".format(
                    self.acceptable_activity_types
                )
            )
        self._activity_type = activity_type

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        components = value.split(" ")
        if len(components) < 5:
            raise ValueError("Address is too short, seems to be missing components.")
        if not (
            components[-3].lower() == "portland," and components[-2].lower() == "or"
        ):
            raise ValueError("Address must be in Portland, OR.")
        zip_code = components[-1]
        if not zip_code.startswith("97"):
            raise ValueError("ZIP code must start with '97'.")
        self._address = value

    @property
    def neighborhood(self):
        return self._neighborhood

    @neighborhood.setter
    def neighborhood(self, value):
        if not isinstance(value, str):
            raise TypeError("Neighborhood must be strings")
        elif not 5 <= len(value) <= 30:
            raise AttributeError(
                "Neighborhood must be at least 5 character and no more than 30"
            )
        else:
            self._neighborhood = value.lower()

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        if website is not None and not isinstance(website, str):
            valid_schemes = ("http://", "https://", "www.", "")
            if not any(website.startswith(scheme) for scheme in valid_schemes):
                raise ValueError(
                    "Website URL must start with 'http://', 'https://', 'www.', or be empty"
                )
        self._website = website

    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {cls.pascal_to_camel_plural()} (
                        id INTEGER PRIMARY KEY,
                        name TEXT, 
                        description TEXT, 
                        activity_type TEXT,
                        address TEXT, 
                        neighborhood TEXT,
                        website TEXT
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
                        (name, description, activity_type, address, neighborhood, website)
                        VALUES
                        (?, ?, ?, ?, ?, ?);
                    """,
                    (
                        self.name,
                        self.description,
                        self.activity_type,
                        self.address,
                        self.neighborhood,
                        self.website,
                    ),
                )
            self.id = CURSOR.lastrowid
            return self
        except Exception as e:
            return e

    @classmethod
    def find_by_neighborhood(cls, neighborhood):
        try:
            with CONN:
                query = f"SELECT * FROM {cls.pascal_to_camel_plural()} WHERE neighborhood = ?"
                result = CURSOR.execute(query, (neighborhood,))
                rows = result.fetchall()
                return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            return e

    @classmethod
    def find_by_rating(cls, rating):
        try:
            return [
                activity
                for activity in cls.get_all()
                if activity.get_rating() == rating
            ]

        except Exception as e:
            return e

    @classmethod
    def find_by_type(cls, activity_type):
        try:
            with CONN:
                query = f"SELECT * FROM {cls.pascal_to_camel_plural()} WHERE activity_type = ?"
                result = CURSOR.execute(query, (activity_type,))
                rows = result.fetchall()
                return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            return e

    @classmethod
    def instance_from_db(cls, row):
        activity = cls.all.get(row[0])
        if activity:
            activity.name = row[1]
            activity.description = row[2]
            activity.activity_type = row[3]
            activity.address = row[4]
            activity.neighborhood = row[5]
            activity.website = row[6]
        else:
            activity = cls(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0])
            cls.all[activity.id] = activity
        return activity

    @classmethod
    def create(
        cls, name, description, activity_type, address, neighborhood, website=None
    ):
        new_activity = cls(
            name, description, activity_type, address, neighborhood, website
        )
        new_activity.save()
        return new_activity

    def get_user_activities(self):
        from models.user_activity import UserActivity

        return [
            user_activity
            for user_activity in UserActivity.get_all()
            if user_activity.activity_id == self.id
        ]

    def get_rating(self):
        ratings = [user_activity.rating for user_activity in self.get_user_activities()]
        return round(sum(ratings) / len(ratings)) if ratings else None
