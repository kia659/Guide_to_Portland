# lib/cli.py

from helpers import (
    welcome,
    exit_program,
    find_or_create_username
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            user = find_or_create_username()
            while True:
                menu()
                choice = input("> ")
                if choice == "0":
                    exit_program()
                elif choice == "1":
                    user = find_or_create_username()
                else:
                    print("Invalid choice")
        else:
            print("Invalid choice")

# def main_menu():
#     print("Please select an option:")
#     print("0. Exit the program")
#     print("1. Browse activities in Portland.")
            



def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create a username.")
    print("2. Browse activities in Portland.")
    print("3. View saved activities.")
    print("4. Delete user.")

if __name__ == "__main__":
    welcome()
    main()


