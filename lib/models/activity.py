# importing regex for our  address validation
import re
from __init__ import CONN, CURSOR


class Activity:

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
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.website = website
        self.address = address
        self.neighborhood = neighborhood

    @property
    def name(self):
        self._name

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
    def activity_type(self):
        self._activity_type

    @activity_type.setter
    def activity_type(self):
        pass

    @property
    def website(self):
        self._activity_type

    @website.setter
    def website(self):
        pass

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        pattern = (
            r"(\d+)\s([NESWnesw]{,2})?\s?([\w\s]+),\s([\w\s]+),\s([A-Za-z]{2})\s(\d{5})"
        )
        if not re.match(pattern, value):
            raise ValueError("Address format must be: 123 S main street , city, stat")
        self._address = value

    # method 1

    # def address(self, value):
    #     # checks for address components
    #     components = value.split(' ')
    #     if len(components) < 5:
    #         raise ValueError("Address is too short, seems to be missing components.")
    #     # is a street number
    #     if not components[0].isdigit():
    #         raise ValueError("Address must start with a street number.")

    #     # looks like a ZIP code (5 digits)
    #     if not (components[-1].isdigit() and len(components[-1]) == 5):
    #         raise ValueError("Address must end with a 5-digit ZIP code.")

    #     self._address = value

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Review instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY UNIQUE,
            name TEXT, 
            description TEXT, 
            activity_type TEXT,
            website TEXT,
            address TEXT, 
            neighborhood TEXT
        """
        CURSOR.execute(sql)
        CONN.commit()

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
