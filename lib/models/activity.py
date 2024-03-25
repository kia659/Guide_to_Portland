from models.__init__ import CONN, CURSOR
from user_activity import UserActivity


class Activity:

    all = {}


    acceptable_activity_types = {
        "free experiences", 
        "food carts", 
        "breweries & bars", 
        "shops", 
        "paid experiences", 
        "restaurants"
    }

    def __init__(
        self,
        name,
        description,
        address,
        neighborhood,
        website,
        activity_type=None,
        id=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.website = website
        self.address = address
        self.neighborhood = neighborhood

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("names must be strings")
        elif not value:
            raise AttributeError("names must be strings with at least one character")
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
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        # checks for address components
        components = value.split(" ")
        if len(components) < 5:
            raise ValueError("Address is too short, seems to be missing components.")
        # is a street number
        if not components[0].isdigit():
            raise ValueError("Address must start with a street number.")
        # is in portland
        if not (
            components[-3].lower() == "portland," and components[-2].lower() == "or"
        ):
            raise ValueError("Address must be in Portland, OR.")
        # looks like a ZIP code (5 digits)
        zip_code = components[-1]
        if not zip_code.startswith("97"):
            raise ValueError("ZIP code must start with '97'.")
        self._address = value

# ask steph should we restrict changing the neighborhood :)
    @property
    def neighborhood(self):
        return self._neighborhood

    @neighborhood.setter
    def neighborhood(self, value):
        if not isinstance(value, str):
            raise TypeError("Neighborhood must be strings")
        elif not 5 <= len(value) <= 15:
            raise AttributeError("Neighborhood must be at least 5 character and no more than 15")
        else:
            self._neighborhood = value

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        if website is not None and not (
            website.startswith("http://") or website.startswith("https://")
        ):
            raise ValueError(
                "Invalid URL. URL must start with 'http://' or 'https://'."
            )
        self._website = website

# TEST ME
    @property
    def activity_type(self):
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        if activity_type.lower() not in self.acceptable_activity_types:
            raise ValueError("Invalid activity type. Please choose from: {}".format(self.acceptable_activity_types))
        self._activity_type = activity_type

    def user_ratings(self):
        return [
            user_activity.rating
            for user_activity in UserActivity.all.values()
            if user_activity.activity_id == self.id and user_activity.rating is not None
        ]

    def average_rating(self):
        ratings = self.user_ratings()
        return sum(ratings) / len(ratings) or None

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Review instances"""
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                name TEXT, 
                description TEXT, 
                activity_type TEXT,
                website TEXT,
                address TEXT, 
                neighborhood TEXT
                )
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            return e

    @classmethod
    def drop_table(cls):
        """Create a new table to persist the attributes of Review instances"""
        try:
            sql = """
                DROP TABLE IF EXISTS activities
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            CONN.rollback()
            return e

    def save(self):
        sql = """
                INSERT INTO activities (name, description, activity_type, website, address, neighborhood)
                VALUES (?, ?, ?, ?, ?, ?)
        """

        CURSOR.execute(
            sql,
            (
                self.name,
                self.description,
                self.activity_type,
                self.website,
                self.address,
                self.neighborhood,
            ),
        )
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

