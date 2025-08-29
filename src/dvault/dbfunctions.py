
# Here are all the functions needed to create the database on SQL and fill them up with the necessary data as well as
# executing all the options that the password_manager provides

import sqlite3
from pathlib import Path

def connect():

    # Create db directory if it does not exist
    # Make sure tildes are expanded
    p = Path("~/.dvault").expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    dvault_path = str(p)

    # Attempt to connect to the 'passmdb' SQLite database
    try:
        # Create a connection object to the database
        conn = sqlite3.connect(dvault_path + '/passmdb')

        # Create a cursor object to execute SQL commands
        c = conn.cursor()

        # Return the connection and cursor objects
        return conn, c

    # Catch any exceptions that occur during the connection process
    except Exception as e:
        # Print an error message that includes the exception message
        print(f"Error:'{e}'")


def disconnect():
    try:
        # Connect to the database using the 'connect' function
        conn, c = connect()

        # Close the database connection
        conn.close()

    # Catch any exceptions that occur during the disconnection process
    except Exception as e:
        # Print an error message that includes the exception message
        print(f"Error:'{e}'")


def create_tables():
    # Connect to the database
    conn, c = connect()

    # Check if 'user' table exists in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    result = c.fetchone()

    if result is None:
        # If 'user' table doesn't exist, create both tables

        # Create 'user' table
        c.execute('''
                CREATE TABLE "user" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "username" NOT NULL,
                "master_password" TEXT NOT NULL,
                "key" BLOB NOT NULL
                );
            ''')

        # Create 'accounts' table
        c.execute(''' 
                CREATE TABLE "accounts"(
                "service" TEXT NOT NULL,
                "username",
                "user_email",
                "web_page" TEXT,
                "password" TEXT NOT NULL,
                "user_id" INT NOT NULL,
                CONSTRAINT fk_users
                FOREIGN KEY ("user_id")
                REFERENCES "user"("id")
                );
            ''')

    else:
        # If 'user' table exists, do nothing
        pass

    # Commit the changes to the database and disconnect
    conn.commit()
    disconnect()


def get_usernames():
    # Connect to the database
    conn, c = connect()

    # Select all usernames from the 'user' table
    c.execute('SELECT username FROM user')

    # Fetch all the results and assign them to 'user_list'
    user_list = c.fetchall()

    # Commit the changes to the database and disconnect
    conn.commit()
    disconnect()

    # Return the list of usernames
    return user_list


def add_user(username, master_password, key):
    try:
        # Connect to the database
        conn, c = connect()

        # Execute an SQL command to insert a new row into the 'user' table
        c.execute(f'''INSERT INTO user ("username", "master_password", "key") 
            VALUES (?, ?, ?)''', (username, master_password, key))

        # Commit the changes to the database and disconnect
        conn.commit()
        disconnect()

    except Exception as e:
        # If an exception occurs, print an error message
        print(f"Error:'{e}'")


def check_username_exists(username):
    # Define a function that checks if a given username exists in the "user" table
    # Connect to the database and retrieve a cursor
    conn, c = connect()

    # Execute a SQL query to select the username from the "user" table
    # where the username matches the input username
    c.execute('SELECT username FROM user WHERE username = ?', (username,))

    # Fetch the first result of the query
    result = c.fetchone()

    # Commit any changes made to the database and close the connection
    conn.commit()
    disconnect()

    # Return True if the query returned a result, False otherwise
    return result is not None


def get_master_password_hashed(username):
    # Define a function that retrieves the hashed master password for a given username
    try:
        conn, c = connect()

        # Use a parameterized query to select the hashed master password
        # for the given username
        c.execute('SELECT master_password FROM user WHERE username=?', (username,))
        master_password_hashed = c.fetchone()

        conn.commit()
        disconnect()

        # Return the first element of the result tuple (i.e., the hashed master password)
        return master_password_hashed[0]

    except Exception as e:
        print(e)


def get_user_id(username):
    # Define a function that retrieves the ID of a user given their username
    try:
        conn, c = connect()

        # Use a parameterized query to select the user ID for the given username
        c.execute('SELECT id FROM user WHERE username=?', (username,))
        user_id = c.fetchone()

        conn.commit()
        disconnect()

        # If no user ID was found for the given username, return None
        if user_id is None:
            return None

        # Otherwise, return the first element of the result tuple (i.e., the user ID)
        return user_id[0]

    except Exception as e:
        # If an exception occurred, print an error message that includes the exception details
        print(f"Error during deletion: '{e}'")


def delete_user(user_id):
    conn, c = connect()

    # Use a parameterized query to check if a user with the given user ID exists in the user table
    c.execute('SELECT id FROM user WHERE id=?', (user_id,))

    # Fetch the result of the query and store it in a variable
    user_exists = c.fetchone()

    # If no user was found with the given user ID, return without deleting anything
    if user_exists is None:
        return

    # Otherwise, delete the user from the user table and all their associated accounts from the accounts table
    c.execute('DELETE FROM user WHERE id=?', (user_id,))
    c.execute('DELETE FROM accounts WHERE user_id=?', (user_id,))

    # Commit the changes and close the connection
    conn.commit()
    disconnect()


def delete_account_table(service, user_id):
    # Connect to the database
    conn, c = connect()

    # Check if the table exists in the database
    c.execute('SELECT user_id FROM accounts WHERE service=?', (service,))
    result = c.fetchone()

    if result is None:
        # If 'accounts' table doesn't exist, show an error message
        print("\nNo data found with that service!")

    else:
        # If the user has the necessary permissions, delete all data related to the service
        c.execute('DELETE FROM accounts WHERE service=? AND user_id=?', (service, user_id))
        print("The service was deleted successfully!")

    # Commit the changes to the database and disconnect
    conn.commit()
    conn.close()


def list_services(user_id):
    # Define a function to list the services saved for a given user ID
    # Try to connect to the database and retrieve the services associated with the user ID
    try:
        conn, c = connect()

        # Use a parameterized query to select the service column from the accounts table
        # where the user ID matches the given user ID
        c.execute('SELECT service FROM accounts WHERE user_id=?', (user_id,))
        services = c.fetchall()

        # If there are no services associated with the user ID, print a message indicating that
        if len(services) == 0:
            print("There are no services yet")
        else:
            # Otherwise, print a message indicating the services associated with the user ID
            print("The following services are saved:")
            for service in services:
                print(service[0])

        # Close the database connection
        conn.close()

    except Exception as e:
        # If there's an error, print an error message
        print(f"Error:'{e}'")


def get_key(user_id):
    # Define a function to get the encrypted key of a user
    # This function can be used during the log in process, for example
    # Try to connect to the database and retrieve the encrypted key associated with the user ID
    try:
        conn, c = connect()

        # Convert the user ID to an integer, then use a parameterized query to select the key column
        # from the user table where the ID matches the given user ID
        user_id = int(user_id)
        c.execute(f'SELECT key FROM user WHERE id=?', (user_id,))

        # Retrieve the user key from the query result and remove the first two characters (the "b" prefix)
        user_key = c.fetchone()[0]
        user_key = user_key[2:]

        # Commit the changes to the database and close the connection
        conn.commit()
        disconnect()

        # Return the user key
        return user_key

    except Exception as e:
        # If there's an error, print an error message
        print(f"Error:'{e}'")


def add_account(service, username, user_email, web_page, password, user_id):
    # Function to add a new account to the "accounts" table

    try:
        conn, c = connect()

        # Execute the SQL INSERT statement to add the account to the table
        c.execute(f'''
            INSERT INTO accounts (service, username, user_email, web_page, password, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (service, username, user_email, web_page, password, user_id))

        # Commit the transaction
        conn.commit()

    except Exception as e:
        # If an error occurs, print the error message
        print(f"Error: {e}")

    finally:
        # Close the database connection
        disconnect()


def show_account_data(service, user_id):
    # This function shows the data of a specific service for a given user
    # It retrieves the data for the service with the given name and the given user id.

    try:
        conn, c = connect()

        c.execute(f'''
            SELECT service, username, user_email, web_page, password 
            FROM accounts
            WHERE user_id=?
            AND service=?  
            ''', (user_id, service))

        # Retrieve the results of the query
        results = c.fetchone()

        conn.commit()
        disconnect()

        if results:
            # If there are results, return the service, username, email, web page, and password
            return results[0], results[1], results[2], results[3], results[4]
        else:
            # If there are no results, return None
            return None

    except Exception as e:
        print(f"Error:'{e}'")


def update_account_service(user_id, service, new_service):
    # Update the "service" of an account from the "accounts" table
    # Find the account by user_id and current service name
    # Change the service name to new_service

    try:
        conn, c = connect()

        c.execute(f'''
            UPDATE accounts
            SET service=?
            WHERE user_id=?
            AND service=?
            ''', (new_service, user_id, service))

        conn.commit()
        disconnect()

        print("Service was updated!")

    except Exception as e:
        print(f"Error:'{e}'")


def check_service(user_id, service):
    # This function checks if a user has a specific service associated with their account.
    try:
        # Call the connect function to establish a connection to a database.
        conn, c = connect()

        # Execute a SQL query to count the number of accounts with a given user_id and service.
        c.execute(f'''
            SELECT COUNT(*) FROM accounts
            WHERE user_id="{user_id}"
            AND service="{service}"
            ''')

        # Get the result of the query and extract the first element (the count).
        result = c.fetchone()[0]

        # Commit the transaction and close the database connection.
        conn.commit()
        disconnect()

        # Return True if the count is greater than 0 (i.e., the user has the service), otherwise False.
        return result > 0

    # If an exception occurs during the execution of the function, print an error message and return False.
    except Exception as e:
        print(f"Error:'{e}'")
        return False


def update_account_username(user_id, service, new_username):
    # This function updates the username for a given user_id and service in the "accounts" table.
    try:
        # Call the connect function to establish a connection to a database.
        conn, c = connect()

        # Execute a SQL query to update the username of the account with the given user_id and service.
        # The new username is passed as a parameter using a parameterized query to prevent SQL injection attacks.
        c.execute(f'''
            UPDATE accounts
            SET username=?
            WHERE user_id=?
            AND service=?
            ''', (new_username, user_id, service))

        # Commit the transaction and close the database connection.
        conn.commit()
        disconnect()

        # Print a message indicating that the username was successfully updated.
        print("Username was updated!")

    # If an exception occurs during the execution of the function, print an error message.
    except Exception as e:
        print(f"Error:'{e}'")


def update_account_user_email(user_id, service, new_email):
    # This function updates the user_email for a given user_id and service in the "accounts" table.
    try:
        # Call the connect function to establish a connection to a database.
        conn, c = connect()

        # Execute a SQL query to update the user_email of the account with the given user_id and service.
        # The new email is passed as a parameter using a parameterized query to prevent SQL injection attacks.
        c.execute(f'''
            UPDATE accounts
            SET user_email=?
            WHERE user_id=?
            AND service=?
            ''', (new_email, user_id, service))

        # Commit the transaction and close the database connection.
        conn.commit()
        disconnect()

        # Print a message indicating that the email was successfully updated.
        print("Email was updated!")

    # If an exception occurs during the execution of the function, print an error message.
    except Exception as e:
        print(f"Error:'{e}'")


def update_account_web_page(user_id, service, new_webpage):
    try:
        # Call the connect function to establish a connection to a database.
        conn, c = connect()

        # Execute a SQL query to update the web_page of the account with the given user_id and service.
        # The new webpage is passed as a parameter using a parameterized query to prevent SQL injection attacks.
        c.execute(f'''
            UPDATE accounts
            SET web_page=?
            WHERE user_id=?
            AND service=?
            ''', (new_webpage, user_id, service))

        # Commit the transaction and close the database connection.
        conn.commit()
        disconnect()

        # Print a message indicating that the webpage was successfully updated.
        print("Website was updated!")

    # If an exception occurs during the execution of the function, print an error message.
    except Exception as e:
        print(f"Error:'{e}'")


def update_account_password(user_id, service, new_password):
    # This function updates the password for a given user_id and service in the "accounts" table.
    try:
        # Call the connect function to establish a connection to a database.
        conn, c = connect()

        # Execute a SQL query to update the password of the account with the given user_id and service.
        # The new password is passed as a parameter using a parameterized query to prevent SQL injection attacks.
        c.execute(f'''
            UPDATE accounts
            SET password=?
            WHERE user_id=?
            AND service=?
            ''', (new_password, user_id, service))

        # Commit the transaction and close the database connection.
        conn.commit()
        disconnect()

        # Print a message indicating that the password was successfully updated.
        print("Password was updated!")

    # If an exception occurs during the execution of the function, print an error message.
    except Exception as e:
        print(f"Error:'{e}'")
