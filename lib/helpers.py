# lib/helpers.py
import os
from rich.console import Console
from rich.console import Theme
from rich.table import Table
from datetime import datetime

from models.activity import Activity
from models.user import User
from models.user_activity import UserActivity


custom_theme = Theme(
    {
        "heading": "bright_white",
        "table_head": "bright_white",  # color of text in the table rows, except for 1st line
        "subhead": "bright_white",
        # "tile": "bold gold3 on blue1",
        # "table": "on blue1"
    }
)

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
    print("Welcome to our insider's guide to Portland!")

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
    table.add_column("Description", style="table_head", width=60)
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")

    activities = Activity.get_all()
    for activity in activities:
        table.add_row(
            activity.name,
            activity.description,
            activity.activity_type,
            activity.address,
            activity.neighborhood,
            activity.website,
        )
    console.print(table)


def view_saved_activities(user):
    table = Table(title="Portland Activities", border_style="black", show_lines=True)
    table.add_column("Name", style="table_head")
    table.add_column("Description", style="table_head", width=60)
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")

    saved_activities = user.get_saved_activities()
    if saved_activities:
        print("Saved Activities:")
        for activity in saved_activities:
            table.add_row(
                activity.name,
                activity.description,
                activity.activity_type,
                activity.address,
                activity.neighborhood,
                activity.website,
            )
        console.print(table)
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


# SUB MENU 2


def find_activity_by_type():
    table = Table(title="Portland Activities", border_style="black", show_lines=True)
    table.add_column("Name", style="table_head")
    table.add_column("Description", style="table_head", width=60)
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")

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

            if 1 <= choice <= len(activity_types):
                selected_activity_type = activity_types[choice - 1]
                activities = Activity.find_by_type(selected_activity_type)
                if activities:
                    print(f"Here are the '{selected_activity_type}':")
                    for activity in activities:
                        table.add_row(
                            activity.name,
                            activity.description,
                            activity.activity_type,
                            activity.address,
                            activity.neighborhood,
                            activity.website,
                        )
                    console.print(table)
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
    table = Table(title="Portland Activities", border_style="black", show_lines=True)
    table.add_column("Name", style="table_head")
    table.add_column("Description", style="table_head", width=60)
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")
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
    table = Table(title="Portland Activities", border_style="black", show_lines=True)
    table.add_column("Name", style="table_head")
    table.add_column("Description", style="table_head", width=60)
    table.add_column("Activity Type", style="table_head")
    table.add_column("Address", style="table_head")
    table.add_column("Neighborhood", style="table_head")
    table.add_column("Website", style="table_head")

    rating = int(input("Enter the rating 1 - 5: "))
    activities = Activity.find_by_rating(rating)
    if activities:
        print(f"Activities with rating '{rating}':")
        for activity in activities:
            table.add_row(
                activity.name,
                activity.description,
                activity.activity_type,
                activity.address,
                activity.neighborhood,
                activity.website,
            )
        console.print(table)
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
    while True:
        try:
            name = input("Enter the name of the activity: ").strip()
            if not name:
                print("Error: Name must be a string with at least one character.")
                continue
            while True:
                description = input("Enter the description of the activity: ").strip()
                if not description:
                    print(
                        "Error: Description must be a string with at least one character."
                    )
                    continue
                while True:
                    print("Activity types:")
                    print("1. Free Experiences")
                    print("2. Food Carts")
                    print("3. Breweries & Bars")
                    print("4. Shops")
                    print("5. Paid Experiences")
                    print("6. Restaurants")

                    activity_type_option = input(
                        "Choose the activity type (enter the corresponding number): "
                    ).strip()
                    if not activity_type_option.isdigit():
                        print("Error: Invalid input. Please enter a number.")
                        continue
                    activity_type_option = int(activity_type_option)
                    if activity_type_option not in range(1, 7):
                        print("Error: Invalid activity type option.")
                        continue
                    activity_types = [
                        "Free Experiences",
                        "Food Carts",
                        "Breweries & Bars",
                        "Shops",
                        "Paid Experiences",
                        "Restaurants",
                    ]
                    activity_type = activity_types[activity_type_option - 1]
                    while True:
                        address = input("Enter the address of the activity: ").strip()
                        components = address.split(" ")
                        if len(components) < 5:
                            print(
                                "Error: Address is too short, seems to be missing components."
                            )
                            continue
                        if not (
                            components[-3].lower() == "portland,"
                            and components[-2].lower() == "or"
                        ):
                            print("Error: Address must be in Portland, OR.")
                            continue
                        zip_code = components[-1]
                        if not zip_code.startswith("97"):
                            print("Error: ZIP code must start with '97'.")
                            continue
                        while True:
                            neighborhood = input(
                                "Enter the neighborhood of the activity. Examples of neighborhoods in Portland: Hawthorne, Northwest District, Pearl District, Clinton: "
                            ).strip()
                            if len(neighborhood) < 5 or len(neighborhood) > 30:
                                print(
                                    "Error: Neighborhood must be between 5 and 30 characters."
                                )
                                continue
                            while True:
                                website = input(
                                    "Enter the website of the activity (optional, press Enter to skip). Website URL must start with 'http://', 'https://', 'www.': "
                                ).strip()
                                break
                            new_activity = Activity.create(
                                name,
                                description,
                                activity_type,
                                address,
                                neighborhood,
                                website,
                            )
                            print("New activity successfully added!")
                            return new_activity
        except Exception as e:
            print(f"Error adding new activity: {e}")
            return None


# SUB MENU 3


def update_rating_review_activity(user):
    activity_id = int(input("Enter the activity id:"))
    activity = UserActivity.find_by_user_name_activity(activity_id, user.id)
    if activity:
        try:
            new_rating = int(
                input(
                    "Enter the rating, must be between 1 (lowest) and 5 (Highest) : "
                ).strip()
            )
            if not 1 <= new_rating <= 5:
                raise ValueError(
                    "Rating must be a valid integer between 1 (lowest) and 5 (Highest)."
                )

            new_review = input("Enter the Review: ").strip()
            if not isinstance(new_review, str) or len(new_review) < 4:
                raise ValueError(
                    "Review must be a string with a minimum of 4 characters."
                )

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
