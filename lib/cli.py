# lib/cli.py

from helpers import (
    welcome,
    exit_program,
    find_or_create_username
)

def main():
    while True:
        main_menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            user = find_or_create_username()
            # START OF SUB MENU 1 - CREATED USERNAME
            while True:
                sub_menu_1()
                choice = input("> ")
                if choice == "0":
                    exit_program()
                elif choice == "1":
                    # Browse activities in Portland. Kia
                    pass
                elif choice == "2":
                    # View saved activities. Xen
                    pass
                elif choice == "3":
                    # Delete user. Steph
                    pass
                else:
                    print("Invalid choice")
            # END OF SUB MENU 1
        else:
            print("Invalid choice")



# Starting program
def main_menu():
    print("To get started, please create a username:")
    print("0. Exit the program")
    print("1. Create a username.")

# After create username
def sub_menu_1():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Browse activities in Portland.")
    print("2. View saved activities.")
    print("3. Delete user.")

# Clicked "Browse Activities"
def sub_menu_2():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Browse all activities.")
    print("2. Find activities by type.")
    print("3. Find activities by name.")
    print("4. Find activities by neighborhood.")
    print("5. Find by rating.")
    print("6. View saved activities.")

# Clicked "View Saved Activities"
def sub_menu_3():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View all saved activities.")
    print("2. Add rating & review to activity.")
    print("3. Delete activity from saved list.")
    print("4. Browse all activities.")
            

if __name__ == "__main__":
    welcome()
    main_menu()


