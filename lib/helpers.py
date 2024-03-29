# lib/helpers.py

import os
from rich.console import Console
from rich.console import Theme
from rich.table import Table
import ipdb
from datetime import datetime

import ipdb
from models.activity import Activity
from models.user import User
from models.user_activity import UserActivity

custom_theme = Theme({
    "heading": "bright_white",
    "table_head": "bright_white",
    "subhead": "turquoise2",
    # "tile": "bold gold3 on blue1",
    # "table": "on blue1"
})
console = Console(theme=custom_theme)

EXIT_WORDS = ["0", "exit", "quit"]


def welcome():
    print(
        """
      _______  __    __   __   _______   _______    .___________.  ______      .______    _______  ___   ___
     /  _____||  |  |  | |  | |       \ |   ____|   |           | /  __  \     |   _  \  |       \ \  \ /  /
    |  |  __  |  |  |  | |  | |  .--.  ||  |__      `---|  |----`|  |  |  |    |  |_)  | |  .--.  | \  V  / 
    |  | |_ | |  |  |  | |  | |  |  |  ||   __|         |  |     |  |  |  |    |   ___/  |  |  |  |  >   <  
    |  |__| | |  `--'  | |  | |  '--'  ||  |____        |  |     |  `--'  |    |  |      |  '--'  | /  .  \ 
     \______|  \______/  |__| |_______/ |_______|       |__|      \______/     | _|      |_______/ /__/ \__\   
          
          """
    )


def exit_program():
    console.print("See ya! Hope you enjoy exploring Portland!", style="subhead")
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


# SUB MENU 1


def browse_all_activities():
    table = Table(title="Portland Activities", border_style="black", show_lines=True)
    table.add_column("Name", style="table_head")
    table.add_column("Description", style="table_head")
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")
    
    activities = Activity.get_all()
    for activity in activities:
        table.add_row(activity.name, activity.description, activity.activity_type, activity.address, activity.neighborhood, activity.website)
    
    console.print(table)

        # attrs = vars(activity)
        # for attr, value in attrs.items():
        #     print(f"{attr}: {value}")
    

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


def delete_user(user):
    # while True: # Loop until 'delete' is provided or the user chooses to exit
    confirmation = input("Please type 'delete' to confirm user deletion: ").strip()

    found_user = User.find_by_name(user.user_name)

    if confirmation == "delete":
        if found_user:
            found_user.delete()
            print(f"You have successfully deleted username: {user.user_name}")
        else:
            print(f"Could not find {user.user_name}.")
    else:
        print(f"Deletion confirmation failed. Please try again.")


# def delete_user():
#     user_name = input("Enter your username to confirm deletion: ").strip()

#     user = User.find_by_name(user_name)
#     if user:
#         user.delete()
#         print(f"You have successfully deleted username: {user_name}")
#     else:
#         print(f"Could not find {user_name}.")


# SUB MENU 2


def find_activity_by_type():
    activity_types = [
        "Free Experiences",
        "Food Carts",
        "Breweries & Bars",
        "Shops",
        "Paid Experiences",
        "Restaurants",
    ]

    print("Activity type options:")
    for i, activity_type in enumerate(activity_types, start=1):
        print(f"{i}. {activity_type}")

    while True:  # Loop until a valid username is provided or the user chooses to exit
        try:
            choice = int(
                input("Enter the number for the type of activity you'd like to see: ")
            )

            # if choice in EXIT_WORDS:
            #     exit_program()

            if 1 <= choice <= len(activity_types):
                selected_activity_type = activity_types[
                    choice - 1
                ].lower()  # Convert to lowercase
                activities = Activity.find_by_type(selected_activity_type)
                if activities:
                    print(f"Here are the '{selected_activity_type}':")
                    for activity in activities:
                        attrs = vars(activity)
                        for attr, value in attrs.items():
                            print(f"{attr}: {value}")
                    return choice  # Exit loop after displaying activities
                else:
                    print(f"No activities of type '{selected_activity_type}' found.")
            else:
                print(
                    "Invalid choice. Please enter a number corresponding to an activity type."
                )
                # return choice # Exit loop if no activities found
        except ValueError:
            print("Invalid input. Please enter a number.")


def find_activity_by_neighborhood():
    print(
        "Examples of neighborhoods in Portland: Hawthorne, Northwest District, Buckman, Clinton, Pearl District, Arlington Heights"
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


def save_to_activities(user):
    try:
        saved_activity_id = int(
            input("Enter the id # for the activity you would like to save: ")
        )
        activity = Activity.find_by_id(saved_activity_id)
        if activity:
            if activity not in user.get_saved_activities():
                UserActivity.create(user.id, saved_activity_id, datetime.now())
                print("Activity has been saved!")
            else:
                print("You've already saved this activity.")
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


# SUB MENU 3


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

            activity.update_rating_and_review(new_review, new_rating)
            print(f"Success: activity id {activity_id} has been updated")
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
