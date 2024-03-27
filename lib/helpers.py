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
        user = User.create(user.user_name)
        print(f'Hi, {user_name}!')
    else:
        print(f"Welcome back, {user.user_name}!")
    return user

def delete_user():
    user_name = input("Enter your username: ").strip()
    
    user = User.find_by_name(user_name)
    if user:
        user.delete()
    else:
        print(f"Could not find {user_name}.")



 # def print_rating(self):
    #     rate_level_emojis = "⭐️" * self.rating if self.rating else None
    #     print(f"{self.name} (ID: {self.activity_id}) | Rating: {rate_level_emojis}")