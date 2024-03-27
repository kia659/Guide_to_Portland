# lib/helpers.py

from models.user import User
from models.activity import Activity
from models.user_activity import UserActivity

def welcome():
    print("""""
      _______  __    __   __   _______   _______    .___________.  ______      .______    _______  ___   ___
     /  _____||  |  |  | |  | |       \ |   ____|   |           | /  __  \     |   _  \  |       \ \  \ /  /
    |  |  __  |  |  |  | |  | |  .--.  ||  |__      `---|  |----`|  |  |  |    |  |_)  | |  .--.  | \  V  / 
    |  | |_ | |  |  |  | |  | |  |  |  ||   __|         |  |     |  |  |  |    |   ___/  |  |  |  |  >   <  
    |  |__| | |  `--'  | |  | |  '--'  ||  |____        |  |     |  `--'  |    |  |      |  '--'  | /  .  \ 
     \______|  \______/  |__| |_______/ |_______|       |__|      \______/     | _|      |_______/ /__/ \__\   
          
          """)

def exit_program():
    print("Goodbye!")
    exit()

def find_or_create_username():
    user_name = input("Enter your username: ").strip()
    
    user = User.find_by_name(user_name)
    
    if user is None:
        user = User.create(user_name)
        print(f'Hi, {user_name}!')
    else:
        print(f"Welcome back, {user_name}!")
    return user

def browse_all_activities():
    activities = Activity.get_all()
    for activity in activities:
        print(activity)

def saved_activities():
    saved_activities = User.get_saved_user_activities()
    if saved_activities:
        print("Saved Activities:")
        for activity in saved_activities:
            print(activity.name)
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
        activity_type = input("Enter the activity type: ")
        activities = Activity.find_by_type(activity_type)
        if activities:
            print(f"Activities of type '{activity_type}':")
            for activity in activities:
                print(activity)
        else:
            print(f"No activities of type '{activity_type}' found.")

def find_activity_by_neighborhood():
        neighborhood = input("Enter the neighborhood: ")
        activities = Activity.find_by_neighborhood(neighborhood)
        if activities:
            print(f"Activities in '{neighborhood}':")
            for activity in activities:
                print(activity)
        else:
            print(f"No activities found in '{neighborhood}'.")

def find_activity_by_rating():
        rating = int(input("Enter the rating: "))
        activities = Activity.find_by_rating(rating)
        if activities:
            print(f"Activities with rating '{rating}':")
            for activity in activities:
                print(activity)
        else:
            print(f"No activities with rating '{rating}' found.")

def save_to_activities():
    pass

def add_new_activity():
    pass









    
def updaterating_review_activity():
    id = input("Enter the activity id:")
    if activity := UserActivity.findby_id(id):
        try:
            review = input("Enter the Review: ")
            activity.review = review
            rating = input(
                "Enter the rating, must be between 1 (lowest) and 5 (Highest) : "
            )
            activity.rating = rating

            activity.updaterating_and_review()
            print(f"Success: {activity}")
        except Exception as exc:
            print("Error updating rating and review: ", exc)
    else:
        print(f"Activity {id} not found")


 # def print_rating(self):
    #     rate_level_emojis = "⭐️" * self.rating if self.rating else None
    #     print(f"{self.name} (ID: {self.activity_id}) | Rating: {rate_level_emojis}")