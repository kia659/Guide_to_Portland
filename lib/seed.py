import csv
import sqlite3
from models.activity import Activity
import ipdb
from random import sample
from datetime import datetime
from models.user import User
from models.user_activity import UserActivity


class SeedDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def seed_from_csv(self, csv_file):
        if not self.connection:
            raise RuntimeError("Database connection not established.")

        # Opens the CSV file for reading as a text file, ensuring it is UTF-8 encoded, and handling newline characters appropriately
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            # Creates a CSV reader object (reader) using DictReader, which interprets each row of the CSV file as a dictionary where keys are column headers and values are cell values
            reader = csv.DictReader(file)
            cursor = self.connection.cursor()
            import ipdb

            activities = []
            for index, row in enumerate(reader):
                values = row.values()
                a = Activity.create(*values)
                activities.append(a)

            kia = User.create("kia")
            ipdb.set_trace()
            kia_activity = UserActivity(
                kia.id,
                sample(activities, 1)[0].id,
                datetime.now(),
                "ehh, it was ok.",
                2,
            )
            kia_activity.save()
            steph = User.create("steph")
            steph_activity = UserActivity(
                steph.id, sample(activities, 1)[0].id, datetime.now(), "So fun!", 5
            )
            steph_activity.save()
            steph_activity2 = UserActivity(
                steph.id,
                sample(activities, 1)[0].id,
                datetime.now(),
                "Really enjoyed this!",
                5,
            )
            steph_activity2.save()

            xen = User.create("xen")
            xen_activity = UserActivity(
                xen.id,
                sample(activities, 1)[0].id,
                datetime.now(),
                "we had a great time!",
                5,
            )
            xen_activity.save()
            matteo = User.create("matteo")
            matteo_activity = UserActivity(
                matteo.id, sample(activities, 1)[0].id, datetime.now(), "awesome!", 5
            )
            matteo_activity.save()
            matteo_activity2 = UserActivity(
                matteo.id, sample(activities, 1)[0].id, datetime.now(), "loved this!", 4
            )
            matteo_activity2.save()
            # cursor.execute(
            #     "INSERT INTO activities (name, description, activity_type, website, address, neighborhood) VALUES (?, ?, ?, ?, ?, ?)",
            #     (row['name'], row['description'], row['activity_type'], row['website'], row['address'], row['neighborhood'])
            # )
            # self.connection.commit()


# Checks if the script is being run directly as the main program
if __name__ == "__main__":
    UserActivity.drop_table()
    User.drop_table()
    Activity.drop_table()

    User.create_table()
    Activity.create_table()
    UserActivity.create_table()
    db_file = "database.db"
    csv_file = "lib/portland_guide_seed_data.csv"

    with SeedDatabase(db_file) as seed_db:
        seed_db.seed_from_csv(csv_file)
