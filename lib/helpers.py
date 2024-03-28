# lib/helpers.py

from models.user import User
from models.activity import Activity
from models.user_activity import UserActivity
from datetime import datetime
import os
import ipdb


EXIT_WORDS = ["0", "exit", "quit"]


def welcome():
    print(
        """""
      _______  __    __   __   _______   _______    .___________.  ______      .______    _______  ___   ___
     /  _____||  |  |  | |  | |       \ |   ____|   |           | /  __  \     |   _  \  |       \ \  \ /  /
    |  |  __  |  |  |  | |  | |  .--.  ||  |__      `---|  |----`|  |  |  |    |  |_)  | |  .--.  | \  V  / 
    |  | |_ | |  |  |  | |  | |  |  |  ||   __|         |  |     |  |  |  |    |   ___/  |  |  |  |  >   <  
    |  |__| | |  `--'  | |  | |  '--'  ||  |____        |  |     |  `--'  |    |  |      |  '--'  | /  .  \ 
     \______|  \______/  |__| |_______/ |_______|       |__|      \______/     | _|      |_______/ /__/ \__\   
          
          """
    )


def exit_program():
    print("See ya! Hope you enjoy exploring Portland!")
    exit()


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# MAIN MENU


def find_or_create_username():
    while True:  # Loop until a valid username is provided or the user chooses to exit
        user_name = input("Enter your username: ").strip()

        if user_name.lower() in EXIT_WORDS:
            exit_program()

        user = User.find_by_name(user_name)

        if user is None:
            try:
                user = User(user_name)
                user.save()
                print(f"Hi, {user_name}!")
                return user  # Exit the loop and return the user object
            except (TypeError, ValueError) as e:
                print(e)
        else:
            print(f"Welcome back, {user_name}!")
            return user  # Exit the loop and return the existing user object


def browse_all_activities():
    activities = Activity.get_all()
    for activity in activities:
        attrs = vars(activity)
        for attr, value in attrs.items():
            print(f"{attr}: {value}")


def view_saved_activities(user):
    saved_activities = user.get_saved_activities()
    if saved_activities:
        print("Saved Activities:")
        for activity in saved_activities:
            activity_attrs = vars(activity)
            for attr, value in activity_attrs.items():
                print(f"{attr}: {value}")
    else:
        print("No saved activities found.")


def delete_user():
    user_name = input("Enter your username: ").strip()

    user = User.find_by_name(user_name)
    if user:
        user.delete()
        print(f"You have successfully deleted username: {user_name}")
    else:
        print(f"Could not find {user_name}.")


# SUB MENU 2


def find_activity_by_type():
    print(
        "Activity type options: Free Experiences, Food Carts, Breweries & Bars, Shops, Paid Experiences, Restaurants"
    )
    activity_type = input("Enter the activity type: ")
    activities = Activity.find_by_type(activity_type)
    if activities:
        print(f"Here are the '{activity_type}':")
        for activity in activities:
            attrs = vars(activity)
            for attr, value in attrs.items():
                print(f"{attr}: {value}")
    else:
        print(f"No activities of type '{activity_type}' found.")


def find_activity_by_neighborhood():
    print(
        "Examples of neighborhoods in Portland: Pearl District, Hawthorne, Alberta, Division, Clinton, Mississippi, St. Johns, Arlington Heights"
    )
    neighborhood = input("Enter the neighborhood: ")
    activities = Activity.find_by_neighborhood(neighborhood)
    if activities:
        print(f"Activities in '{neighborhood}':")
        for activity in activities:
            attrs = vars(activity)
            for attr, value in attrs.items():
                print(f"{attr}: {value}")
    else:
        print(f"No activities found in '{neighborhood}'.")


def find_activity_by_rating():
    rating = int(input("Enter the rating 1 - 5: "))
    activities = Activity.find_by_rating(rating)
    if activities:
        print(f"Activities with rating '{rating}':")
        for activity in activities:
            attrs = vars(activity)
            for attr, value in attrs.items():
                print(f"{attr}: {value}")
    else:
        print(f"No activities with rating '{rating}' found.")

    # rating = int(input("Enter the rating 1 - 5: "))
    # activities = Activity.find_by_rating(rating)
    # if activities:
    #     print(f"Activities with rating '{rating}':")
    #     for activity in activities:
    #         print(activity)
    # else:
    #     print(f"No activities with rating '{rating}' found.")


# Why can input zero?


def save_to_activities(user):
    try:
        total_activities = len(Activity.get_all())

        saved_activity_id = int(
            input("Enter the id # for the activity you would like to save: ")
        )
        if 0 < saved_activity_id <= total_activities:
            UserActivity.create(user.id, saved_activity_id, datetime.now())
            print("Activity has been saved!")
        else:
            print("Error: Please choose a valid id number for the activity.")
    except ValueError:
        print("Error: Please enter a valid integer id number for the activity.")


def add_new_activity():
    try:
        name = input("Enter the name of the activity: ").strip()
        description = input("Enter the description of the activity: ").strip()
        activity_type = input(
            "Enter the type of activity (choose from Free Experiences, Food Carts, Breweries & Bars, Shops, Paid Experiences, Restaurants): "
        ).strip()
        address = input("Enter the address of the activity: ").strip()
        neighborhood = input("Enter the neighborhood of the activity: ").strip()
        website = input(
            "Enter the website of the activity (optional, press Enter to skip): "
        ).strip()

        new_activity = Activity.create(
            name, description, activity_type, address, neighborhood, website
        )

        print("New activity successfully added!")
        return new_activity
    except Exception as e:
        print(f"Error adding new activity: {e}")
        return None


def update_rating_review_activity():
    activity_id = input("Enter the activity id:")
    if activity := UserActivity.findby_id(activity_id):
        try:
            review = input("Enter the Review: ")
            activity.review = review
            rating = input(
                "Enter the rating, must be between 1 (lowest) and 5 (Highest) : "
            )
            activity.rating = rating

            activity.update_rating_and_review()
            print(f"Success: {activity}")
        except Exception as exc:
            print("Error updating rating and review: ", exc)
    else:
        print(f"Activity {activity_id} not found")


def delete_user_activity(user):
    deleted_id = int(input("Activity ID to delete: ").strip())

    delete_activity = UserActivity.find_by_user_name_activity(deleted_id, user.id)
    if delete_activity:
        delete_activity.delete()
        print(f"You have successfully deleted activity: {deleted_id}")
    else:
        print(f"Could not find {deleted_id}.")


# def print_rating(self):
#     rate_level_emojis = "⭐️" * self.rating if self.rating else None
#     print(f"{self.name} (ID: {self.activity_id}) | Rating: {rate_level_emojis}")
