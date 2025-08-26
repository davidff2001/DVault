import sys
import random

from crypto import (generate_hash, generate_key)
from dbfunctions import (create_tables, check_username_exists, add_user, get_master_password_hashed,
                         get_user_id, delete_user, delete_account_table, list_services, add_account,
                         show_account_data, update_account_username, update_account_password,
                         update_account_user_email, update_account_service, check_service, update_account_web_page)


def program_choose_menu():
    # This function will let the user choose between using the "Password Generator" and the "Password Manager"

    print("\n|----------------------------------------------------------------------------|")
    print('|                                                                            |')
    print('|     Welcome to the Secure Password Generator and Password Manager 3.0      |')
    print('|               Developed By David Fernandez, May 2023                       |')
    print('|                                                                            |')
    print('|----------------------------------------------------------------------------|')
    print("\nPlease select one of the options above:")
    # printing out the program options
    print('\nPrograms:')
    print('\n1. Password Generator')
    print('2. Password Manager')
    print('3. Exit')

    # asking the user to choose a program
    choose = input("\nChoose a program:")

    # checking if the user chose the "Password Generator" program
    if choose == "1":
        password_generator()  # calling the password_generator() function
        program_choose_menu()

    # checking if the user chose the "Password Manager" program
    if choose == "2":
        password_manager_menu()  # calling the password_manager_menu() function

    # checking if the user chose the "Exit" program
    if choose == "3":
        sys.exit()  # exiting the program using the exit() function from the sys module

    else:
        # if the user enters an invalid option
        if choose.strip() == "":
            print("\nPlease choose a valid option.")
        else:
            print("\nInvalid option. Please choose a valid option.")
        program_choose_menu()  # calling the program_choose_menu() function again to prompt the user again

    # returning the input from the user (not sure why this is necessary in this code)
    return input()


def password_manager_menu():
    # This menu will let you choose between adding a new user, search for an existing user,delete an existing user,
    # create a new database, and go back

    # printing out the options for the password manager menu
    print("\n|----------------------------|")
    print("|Password Manager 2.0        |")
    print("|                            |")
    print("|Developed by David Fernandez|")
    print("|----------------------------|")
    print("\n|---------------------------|")
    print('|Choose an option:          |')
    print('|1. Add new user            |')
    print('|2. Select an existing user |')
    print('|3. Delete user             |')
    print('|4. Go to programs menu     |')
    print("|---------------------------|\n")

    # asking the user to select an option
    choose = input("Select:")

    # checking if the user chose to add a new user
    if choose == "1":
        create_user()  # calling the create_user() function

    # checking if the user chose to select an existing user
    if choose == "2":
        select_user()  # calling the select_user() function

    # checking if the user chose to delete a user
    if choose == "3":
        delete_user_menu()  # calling the delete_user_menu() function

    # checking if the user chose to go back to the programs menu
    if choose == "4":
        program_choose_menu()  # calling the program_choose_menu() function

    else:
        # if the user enters an invalid option
        if choose.strip() == "":
            print("Please choose an option.")
        else:
            print("Invalid option. Please choose a valid option.")
        password_manager_menu()  # calling the password_manager_menu() function again to prompt the user again

    # returning the input from the user (not sure why this is necessary in this code)
    return input()


def create_user():
    # Create necessary tables in the database
    create_tables()  # calling the create_tables() function to create the necessary tables in the database

    # Ask the user to enter a username and a master password
    print('\nNext you will need to add an username and a master password')
    print('\nPlease do not forget this or you would not be able to access your data')

    # Validate the username input
    valid = False
    while not valid:
        username = input('\nType a username: ')
        if check_username_exists(username):
            print('\nUsername already exists. Please try again.')
        elif not username.strip():
            print('\nUsername cannot be blank. Please try again.')
        else:
            valid = True

    # Validate the master password input
    valid = False
    while not valid:
        master_password = input('Type a master password: ')
        if len(master_password) > 20:
            print('The master password should not exceed 20 characters. Please try again.')
        elif not master_password.strip():
            print('Master password cannot be blank. Please try again.')
        else:
            valid = True

    # Hash the master password and generate a key

    master_password = generate_hash(master_password)  # calling the generate_hash() function to hash the master password

    key = generate_key()  # calling the generate_key() function to generate a key

    # Add the user to the database

    add_user(username, master_password, key)  # calling the add_user() function to add the user to the database
    print('\nUser added successfully!')

    # Redirect the user to the password manager menu

    password_manager_menu()

    # calling the password_manager_menu() function to redirect the user to the password manager menu


def select_user():
    # Prompt user to input username and password
    username = input("\nInsert username:")
    insert_password = input("\nInsert Password:")

    # Check if password length is greater than 20 characters
    if len(insert_password) > 20:
        print("\nPassword length cannot exceed 20 characters")
        password_manager_menu()  # Redirect to password manager menu

    # Hash the input password and retrieve the hashed password from the database for the given username

    given_hash = generate_hash(insert_password)
    stored_hash = get_master_password_hashed(username)

    # Compare the hashed passwords to grant or deny access
    if given_hash == stored_hash:
        print("\nAccess granted.")
        account_menu(username)  # Redirect to account menu
    else:
        print("Access denied")
        password_manager_menu()  # Redirect to password manager menu


def delete_user_menu():
    # This function provides a user interface for deleting a user from a database
    # Display a warning message to the user

    print("THIS IS A WARNING, YOUR A DELETING A USER FROM THE DATABASE")

    # Prompt the user to enter the username and password of the account to be deleted

    username = input("\nInsert username:")
    insert_password = input("\nInsert Password:")

    # If the length of the password entered by the user is greater than 20 characters,
    # display an error message and return to the password manager menu

    if len(insert_password) > 20:
        print("\nPassword length cannot exceed 20 characters")
        password_manager_menu()
        return

    # Get the stored hash of the master password associated with the username entered by the user
    stored_hash = get_master_password_hashed(username)

    # If the stored hash is None, display an error message and return to the password manager menu

    if stored_hash is None:
        print("\nThis user is not stored in the database or no data was introduced")
        password_manager_menu()
        return

    # Generate a hash of the password entered by the user and check if it matches the stored hash

    given_hash = generate_hash(insert_password)
    accessed = given_hash == stored_hash

    # If the password entered by the user matches the stored hash,
    # delete the user from the database and display a success message. Otherwise, display an error message.

    if accessed:
        user_id = get_user_id(username)
        rows_affected = delete_user(user_id)

        if rows_affected is None:
            print("\nUser successfully deleted!")
        else:
            print("Error deleting user")

    else:
        print("\nIncorrect Password")

    # Return to the password manager menu
    password_manager_menu()


def account_menu(username):
    # This function provides a user interface for the account menu, given the username of the account
    # Get the user id associated with the given username
    user_id = get_user_id(username)

    # Display a welcome message and a list of options for the user to choose from
    print(f'\nWelcome {username}')
    print("|-------------------------------|")
    print("|Select option:                 |")
    print("|1. List saved services         |")
    print("|2. Add new data                |")
    print("|3. Get data from a service     |")
    print("|4. Update data from a service  |")
    print("|5. Delete a service            |")
    print("|6. Go to Password Manager menu |")
    print("|-------------------------------|\n")
    choose = input("Select:")

    # Depending on the user's choice, call the appropriate function and return to the account menu
    if choose == "1":
        list_services(user_id)
        account_menu(username)

    elif choose == "2":
        user_id = get_user_id(username)
        add_account_menu(user_id)
        account_menu(username)

    elif choose == "3":
        user_id = get_user_id(username)
        print_account_data(user_id)
        account_menu(username)

    elif choose == "4":
        update_account_menu(user_id, username)
        account_menu(username)

    elif choose == "5":
        delete_service(user_id)
        account_menu(username)

    elif choose == "6":
        password_manager_menu()

    else:
        # If the user enters an invalid choice, display an error message and return to the account menu
        if choose.strip() == "":
            print("Please choose an option.")
        else:
            print("Invalid option. Please choose a valid option.")
        account_menu(username)


def add_account_menu(user_id):
    print("Add new service:")

    # Keep asking for input until a non-empty service is provided
    while True:
        service = input("Service name: ")
        if service.strip() == '':
            print("Service cannot be empty!")
        else:
            break

    if check_service(user_id, service):
        print(f"\nThe service '{service}' already exists. Please enter a different service name.")
        account_menu(user_id)
        return

    else:
        username = input("Username: ")
        user_email = input("Email: ")
        web_page = input("Web page: ")
        password = input("Password: ")

        add_account(service, username, user_email, web_page, password, user_id)

        print("Account added successfully!")


def print_account_data(user_id):
    try:
        # Prompt the user to enter the name of the service they want to check.
        service = input("\nWhat service do you want to check?\n")

        # Check if the user has entered a valid service name. If not, display an error message and return.
        if len(service) == 0:
            print("Service cannot be empty!")
            return

        # Call the show_account_data() function to get the account data for the provided service and user_id.
        results = show_account_data(service, user_id)

        # If no data is found for the provided service, display an appropriate message.
        if results is None:
            print("No data found")

        # If data is found, display the account data for the service.
        else:
            print(f"\nService: {results[0]}")
            print(f"Username: {results[1]}")
            print(f"Email: {results[2]}")
            print(f"Website: {results[3]}")
            print(f"Password: {results[4]}")

    except Exception as e:
        # If an error occurs, display an error message with the details of the error.
        print(f"Error: '{e}'")


def delete_service(user_id):
    # Warn the user about deleting all data related to a service
    print("THIS IS A WARING, YOU ARE GOING TO DELETE ALL THE DATA FROM A SERVICE")

    # Ask the user to input the service to be deleted
    service = input("Type service you want to delete: ")

    # Call the 'delete_account_table' function to delete all data related to the service
    delete_account_table(service, user_id)


def update_account_menu(user_id, username):
    # Display the options for updating the account.
    print("\n|-------------------------------|")
    print("|What do you want to update?    |")
    print("|1. Service                     |")
    print("|2. Username                    |")
    print("|3. Email                       |")
    print("|4. Website                     |")
    print("|5. Password                    |")
    print("|6. Go to Account Menu          |")
    print("|-------------------------------|\n")

    # Prompt the user to select an option.
    choose = input("Select:")

    # Check which option the user selected and call the appropriate function to update the account information.
    if choose == "1":
        update_service_menu(user_id)
        update_account_menu(user_id, username)

    elif choose == "2":
        update_username_menu(user_id)
        update_account_menu(user_id, username)

    elif choose == "3":
        update_email_menu(user_id)
        update_account_menu(user_id, username)

    elif choose == "4":
        update_website_menu(user_id)
        update_account_menu(user_id, username)

    elif choose == "5":
        update_password_menu(user_id)
        update_account_menu(user_id, username)

    elif choose == "6":
        account_menu(username)

    # If the user did not enter a valid option, display an error message and prompt them to choose again.
    else:
        if choose.strip() == "":
            print("Please choose an option.")
        else:
            print("Invalid option. Please choose a valid option.")
        update_account_menu(user_id, username)


def update_service_menu(user_id):
    # Prompt the user to enter the name of the service they want to update and the new service name.
    service = input("Enter the service you want to update: ")
    new_service = input("New service name: ")

    # Check if the new service name is empty, and display an error message if it is.
    if not new_service:
        print("\nService name can't be empty")
        return

    # Check if the new service name already exists for this user, and display an error message if it does.
    if check_service(user_id, new_service):
        print(f"Service '{new_service}' already exists for this user")
        update_account_menu(user_id)
        return

    # If the new service name is valid and doesn't already exist, call the function to update the service name.
    else:
        update_account_service(user_id, service, new_service)


def update_username_menu(user_id):
    # Prompt the user to enter the name of the service they want to update and the new username.
    service = input("Enter the service you want to update: ")
    new_username = input("New username: ")

    # Check if the service name is empty, and display an error message if it is.
    if not service:
        print("Service name can't be empty")
        return

    # If the service name is valid, call the function to update the username.
    else:
        update_account_username(user_id, service, new_username)


def update_email_menu(user_id):
    # Prompt the user to enter the name of the service they want to update and the new email.
    service = input("Enter the service you want to update: ")
    new_email = input("New email: ")

    # Check if the service name is empty, and display an error message if it is.
    if not service:
        print("Service name can't be empty")
        return

    # If the service name is valid, call the function to update the email.
    else:
        update_account_user_email(user_id, service, new_email)


def update_website_menu(user_id):
    # Prompt the user to enter the name of the service they want to update and the new website.
    service = input("Enter the service you want to update: ")
    new_webpage = input("New website: ")

    # Check if the service name is empty, and display an error message if it is.
    if not service:
        print("Service name can't be empty")
        return

    # If the service name is valid, call the function to update the website.
    else:
        update_account_web_page(user_id, service, new_webpage)


def update_password_menu(user_id):
    # Prompt the user to enter the name of the service they want to update and the new password.
    service = input("Enter the service you want to update: ")
    new_password = input("New password: ")

    # Check if the service name is empty, and display an error message if it is.
    if not service:
        print("Service name can't be empty")
        return

    # If the service name is valid, call the function to update the password.
    else:
        update_account_password(user_id, service, new_password)


def password_generator():
    # This function generates a random password with a specified length and a mix of special characters, numbers,
    # upper and lower case letters.
    # Print a welcome message with information about the program and the developer.
    print("\n|----------------------------|")
    print("|Password Generator 2.0      |")
    print("|                            |")
    print("|Developed by David Fernandez|")
    print("|----------------------------|")

    # Define a sequence of characters to use when generating the password.
    char_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?-_:;$&%()/."

    # Prompt the user to enter the desired length of the password.
    length = int(input("\nEnter the required length of the password ranging from 8 to 20: "))

    # If the length is not within the specified range, print an error message and quit the program.
    if not (8 <= length <= 20):
        print("\nEnter a suitable range!\n")
        password_generator()

    # Generate a random password with the specified length and character sequence.
    password = str()
    for _ in range(length):
        random_char = random.choice(char_seq)
        password += random_char

    # Print the generated password.
    print("\nThis is your password: ", password)
