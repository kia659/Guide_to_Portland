# lib/cli.py
from rich.console import Console
from rich.console import Theme
from helpers import (
    welcome,
    exit_program,
    find_or_create_username,
    browse_all_activities,
    view_saved_activities,
    delete_user,
    find_activity_by_type,
    find_activity_by_neighborhood,
    find_activity_by_rating,
    save_to_activities,
    add_new_activity,
    update_rating_review_activity,
    delete_user_activity,
    clear_screen,
)

custom_theme = Theme({
    "heading": "bold bright_white",
    "table_head": "bold bright_white on blue1",
    "subhead": "turquoise2",
    "tile": "bold gold3 on blue1",
    "table": "on blue1"
})
console = Console(theme=custom_theme)

def main():
    while True:
        main_menu()
        choice_main = input("> ")
        if choice_main == "0":
            exit_program()
        elif choice_main == "1":
            user = find_or_create_username()
            # START OF SUB MENU 1 - CREATED USERNAME
            while True:
                sub_menu_1()
                choice_sub_1 = input("> ")
                if choice_sub_1 == "0":
                    exit_program()
                elif choice_sub_1 == "1":
                    clear_screen()
                    browse_all_activities()
                    # START OF SUB MENU 2 - BROWSE ACTIVITIES
                    while True:
                        sub_menu_2()
                        choice_sub_2 = input("> ")
                        if choice_sub_2 == "0":
                            exit_program()
                        elif choice_sub_2 == "1":
                            browse_all_activities()
                        elif choice_sub_2 == "2":
                            clear_screen()
                            find_activity_by_type()
                        elif choice_sub_2 == "3":
                            clear_screen()
                            find_activity_by_neighborhood()
                        elif choice_sub_2 == "4":
                            clear_screen()
                            find_activity_by_rating()
                        elif choice_sub_2 == "5":
                            save_to_activities(user)
                        elif choice_sub_2 == "6":
                            add_new_activity()
                        elif choice_sub_2 == "7":
                            view_saved_activities(user)
                            while True:
                                # START OF SUB MENU 3 - VIEW SAVED ACTIVITIES
                                sub_menu_3()
                                choice_sub_3 = input("> ")
                                if choice_sub_3 == "0":
                                    exit_program()
                                elif choice_sub_3 == "1":
                                    break
                                elif choice_sub_3 == "2":
                                    update_rating_review_activity(user)
                                elif choice_sub_3 == "3":
                                    delete_user_activity(user)
                                else:
                                    print("Invalid choice")
                    # END OF SUB MENU 2
                elif choice_sub_1 == "2":
                    view_saved_activities(user)
                    while True:
                        # START OF SUB MENU 3 - VIEW SAVED ACTIVITIES
                        sub_menu_3()
                        choice_sub_3 = input("> ")
                        if choice_sub_3 == "0":
                            exit_program()
                        elif choice_sub_3 == "1":
                            break
                        elif choice_sub_3 == "2":
                            update_rating_review_activity()
                        elif choice_sub_3 == "3":
                            delete_user_activity(user)
                        else:
                            print("Invalid choice")
                elif choice_sub_1 == "3":
                    clear_screen()
                    delete_user(user)
                    break
                else:
                    print("Invalid choice")
            # END OF SUB MENU 1
        else:
            print("Invalid choice")


# Starting program
def main_menu():
    console.print("To get started, please login or create a username: ", style="subhead")
    print("0. Exit the program.")
    print("1. Create or login with username.")


# After create username
def sub_menu_1():
    console.print("Please select an option:", style="subhead")
    print("0. Exit the program.")
    print("1. Browse activities in Portland.")
    print("2. View all saved activities.")
    print("3. Delete user.")


# Clicked "Browse Activities"
def sub_menu_2():
    console.print("Please select an option:", style="subhead")
    print("0. Exit the program.")
    print("1. Browse all activities.")
    print("2. Find activities by type.")
    print("3. Find activities by neighborhood.")
    print("4. Find by rating.")
    print("5. Save to your activities.")
    print("6. Add a new activity.")
    print("7. View all saved activities.")


# Clicked "View Saved Activities"
def sub_menu_3():
    console.print("Please select an option:", style="subhead")
    print("0. Exit the program.")
    print("1. Return to previous menu.")
    print("2. Add rating & review to activity.")
    print("3. Delete activity from saved list.")
    print("4. Browse all activities.")


if __name__ == "__main__":
    welcome()
    main()
