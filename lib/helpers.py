# lib/helpers.py

from models.user import User
from models.activity import Activity
from models.user_activity import UserActivity
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
    print("Goodbye!")
    exit()


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


def saved_activities(user):
    saved_activities = user.get_saved_activities()
    if saved_activities:
        print("Saved Activities:")
        for activity in saved_activities:
            print(activity)
    else:
        print("No saved activities found.")


def delete_user():
    user_name = input("Enter your username: ").strip()

    user = User.find_by_name(user_name)
    if user:
        user.delete()
    else:
        print(f"Could not find {user_name}.")


# START OF SUB MENU 2


def find_activity_by_type():
    print(
        "Activity type options: Free Experiences, Food Carts, Breweries & Bars, Shops, Paid Experiences, Restaurants"
    )
    activity_type = input("Enter the activity type: ")
    activities = Activity.find_by_type(activity_type)
    if activities:
        print(f"Activities of type '{activity_type}':")
        for activity in activities:
            print(activity)
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
            print(activity)
    else:
        print(f"No activities found in '{neighborhood}'.")


def find_activity_by_rating():
    rating = int(input("Enter the rating 1 - 5: "))
    activities = Activity.rated_activities(rating)
    if activities:
        print(f"Activities with rating '{rating}':")
        for activity in activities:
            print(activity)
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


def save_to_activities():
    pass


def add_new_activity():
    pass


def update_rating_review_activity():
    id = input("Enter the activity id:")
    if activity := UserActivity.findby_id(id):
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
        print(f"Activity {id} not found")


# def print_rating(self):
#     rate_level_emojis = "⭐️" * self.rating if self.rating else None
#     print(f"{self.name} (ID: {self.activity_id}) | Rating: {rate_level_emojis}")
