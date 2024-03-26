from models.__init__ import CONN, CURSOR
from models.helper import Helper
# from models.user_activity import UserActivity
import ipdb


class Activity(Helper):

    all = {}


    acceptable_activity_types = {
        "Free Experiences", 
        "Food Carts", 
        "Breweries & Bars", 
        "Shops", 
        "Paid Experiences", 
        "Restaurants"
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
        elif not 5 <= len(value) <= 30:
            raise AttributeError("Neighborhood must be at least 5 character and no more than 30")
        else:
            self._neighborhood = value

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, website):
        # if not website.startswith("http://") or website.startswith("https://"):
        #     raise ValueError(
        #         "Invalid URL. URL must start with 'http://' or 'https://'."
        #     )
        self._website = website

# TEST ME
    @property
    def activity_type(self):
        return self._activity_type

    @activity_type.setter
    def activity_type(self, activity_type):
        if activity_type not in self.acceptable_activity_types:
            raise ValueError("Invalid activity type. Please choose from: {}".format(self.acceptable_activity_types))
        self._activity_type = activity_type

    # def user_ratings(self):
    #     return [
    #         user_activity.rating
    #         for user_activity in UserActivity.all.values()
    #         if user_activity.activity_id == self.id and user_activity.rating is not None
    #     ]

    # def average_rating(self):
    #     ratings = self.user_ratings()
    #     return sum(ratings) / len(ratings) or None

   

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
        except Exception as e:
            return e

    @classmethod
    def instance_from_db(cls, row):
        activity = cls.all.get(row[0])
        if activity:
            activity.name = row[1]
            activity.description = row[2]
            activity.neighborhood = row[3]
            activity.website = row[4]
            activity.activity_type = row[5]
        else:
            activity = cls(row[1], row[2], row[3], row[4], row[5], id=row[0])
            cls.all[activity.id] = activity
        return activity
    
    @classmethod
    def create(cls, name, description, activity_type, address, neighborhood, website=None):
        # ipdb.set_trace()
        new_activity = cls(name, description, activity_type, address, neighborhood, website)
        new_activity.save()
        return new_activity
    
    # # # Returns a list of the users that have saved the activity
    # # def get_users(self):
    # #     return [user_activity.user for user_activity in UserActivity.all() if user_activity.activity == self]

    # # Returns a list of the user activities the user has saved
    # def get_saved_user_activities(self):
    #     from models.user_activity import UserActivity
    #     return [user_activity for user_activity in UserActivity.all() if user_activity.user_id == self.id]

    # # Returns a list of the activities the user has saved
    # def get_saved_activities(self):
    #     from models.user_activity import UserActivity
    #     return [user_activity.activity for user_activity in self.get_saved_user_activities()]