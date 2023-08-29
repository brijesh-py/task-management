import mysql.connector as mc
import sys


# The `TaskManager` class is a program that allows users to create accounts, login, manage tasks, and
# perform various actions related to task management.
class TaskManager:
    def __init__(self):
        """
        The function initializes a database connection and cursor, creates an authentication table, and
        performs a featured action.
        """
        self.connector = mc.connect(
            host="localhost",
            username="admin",
            password="123456",
            database="databasename",
        )
        self.cursor = self.connector.cursor()
        self.create_auth()
        self.featured()

    def featured(self):
        """
        The `featured` function displays a menu for a task manager program and prompts the user to choose
        an option.
        """
        print(
            """Welcome to Task Manager
              Login for press [1]
              Create Account for press [2]
              Delete Account for press [3]
              Exit for press [4]
              """
        )
        get_input = input("Press Key: ")
        if get_input == "1":
            self.login_user()
        elif get_input == "2":
            self.create_user()
        elif get_input == "3":
            self.delete_account()
        elif get_input == "4":
            self.cursor.close()
            self.connector.close()
            print("Goodbye!")
            sys.exit()
        else:
            self.featured()

    def create_auth(self):
        """
        The function creates two tables in a database, one for users and one for tasks, with specific
        columns and constraints.
        """
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(40) NOT NULL UNIQUE, password VARCHAR(40) NOT NULL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks(id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, title VARCHAR(40) NOT NULL,descs VARCHAR(100) NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))"
        )
        self.connector.commit()

    def check_credentials(self, username, password):
        """
        The function checks if the length of the username is between 5 and 20 characters and the length
        of the password is between 6 and 20 characters, and returns True if both conditions are met.

        :param username: The username parameter is a string that represents the username entered by the
        user
        :param password: The password parameter is a string that represents the password entered by the
        user
        :return: True if the length of the username is between 5 and 20 characters and the length of the
        password is between 6 and 20 characters. If the lengths do not meet these criteria, the function
        is printing a message and calling the `featured()` method.
        """
        if 5 <= len(username) <= 20 and 6 <= len(password) <= 20:
            return True
        else:
            print(
                """Username Length: 5 to 20 characters
                  Password Length: 6 to 20 characters"""
            )
            self.featured()

    def create_user(self):
        """
        The function `create_user` prompts the user to enter a username and password, checks if the
        username already exists in the database, and if not, inserts the new user into the database.
        """
        username = input("Enter username: ").strip()
        password = input("Enter Password: ").strip()
        self.cursor.execute(f"SELECT username FROM users WHERE username='{username}'")
        res = self.cursor.fetchone()
        if res:
            print("User already exists. Try a different username.")
            self.create_user()
        elif self.check_credentials(username, password):
            self.cursor.execute(
                f"INSERT INTO users(username, password) VALUES ('{username}','{password}')"
            )
            self.connector.commit()
            print("User created successfully!")
            self.login_user()

    def login_user(self):
        """
        The `login_user` function prompts the user to enter their username and password, checks if the
        credentials are valid, and then retrieves user information from a database if the credentials are
        correct.
        """
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        if self.check_credentials(username, password):
            self.cursor.execute(
                f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            )
            res = self.cursor.fetchone()
            if res:
                print(f"Welcome, {res[1]}!")
                self.authenticated_featured(res[0])
            else:
                print("Invalid Username or Password. Please try again.")
                self.login_user()

    def authenticated_featured(self, user_id):
        """
        The function `authenticated_featured` displays a menu of options for an authenticated user and
        performs different actions based on the user's input.

        :param user_id: The `user_id` parameter is the unique identifier for the user who is currently
        authenticated and accessing the featured options. It is used to perform actions specific to that
        user, such as showing their profile, updating their account, deleting their account, adding
        tasks, showing tasks, etc
        """
        print(
            """Showing Profile for press [1]
              Update Account for press [2]
              Delete Account for press [3]
              Add Task for press [4]
              Show Tasks for press [5]
              Logout for press [6]
              Exit for press [7]
"""
        )
        get_input = input("Pree Key : ")
        if get_input == "1":
            self.showing_profile(user_id)
        elif get_input == "2":
            self.update_account(user_id)
        elif get_input == "3":
            self.delete_account(user_id)
        elif get_input == "4":
            self.add_task(user_id)
        elif get_input == "5":
            self.show_tasks(user_id)
        elif get_input == "6":
            print("Logout!")
            self.featured()
        elif get_input == "7":
            print("Goodbye!")
            self.connector.close()
            sys.exit()
        else:
            print("Invalid Press Key?")
            self.authenticated_featured(user_id)

    def delete_account(self, user_id):
        """
        The `delete_account` function deletes a user's account and associated tasks from a database.

        :param user_id: The user_id parameter is the unique identifier of the user whose account needs to
        be deleted
        """
        self.cursor.execute(f"DELETE FROM tasks WHERE user_id='{user_id}'")
        self.cursor.execute(f"DELETE FROM users WHERE id='{user_id}'")
        self.connector.commit()
        print("Account deleted successfully!")
        self.featured()

    def update_account(self, user_id):
        """
        The function `update_account` updates the username and password of a user in the database based
        on their user ID.

        :param user_id: The `user_id` parameter is the unique identifier of the user whose account needs
        to be updated
        """
        print("Update Account")
        username = input("Enter Username : ")
        password = input("Enter Password : ")
        self.cursor.execute(
            f"UPDATE users SET username='{username}', password='{password}' WHERE id='{user_id}'"
        )
        self.connector.commit()
        self.authenticated_featured(user_id)

    def showing_profile(self, user_id):
        """
        The function "showing_profile" retrieves user information from a database and prints it, then
        calls another function.

        :param user_id: The `user_id` parameter is the unique identifier of the user whose profile is
        being displayed
        """
        self.cursor.execute("SELECT * FROM users")
        res = self.cursor.fetchone()
        print(f"Id: {res[0]} | username: {res[1]} | password: {res[2]}")
        self.authenticated_featured(user_id)

    def add_task(self, user_id):
        """
        The function `add_task` prompts the user to enter a title and description for a task, checks if
        the length of the title and description are within specified limits, and inserts the task into a
        database if the conditions are met.

        :param user_id: The user_id parameter is the unique identifier for the user who is adding the
        task
        """
        title = input("Enter Title : ")
        desc = input("Enter Description : ")
        if 3 <= len(title) <= 40 and 5 <= len(desc) <= 100:
            self.cursor.execute(
                f"INSERT INTO tasks (user_id, title, descs) VALUES('{user_id}','{title}','{desc}')"
            )
            self.connector.commit()
            print("Sucessfully Added Task!")
            self.authenticated_featured(user_id)
        else:
            print("Title Length MIN 3 & MAX 40 and Description Length MIN 5 & MAX 100!")
            self.add_task(user_id)

    def show_tasks(self, user_id):
        """
        The function `show_tasks` retrieves and displays tasks associated with a specific user ID from a
        database.

        :param user_id: The user_id parameter is the unique identifier for a user. It is used to filter
        the tasks table and retrieve only the tasks associated with that specific user
        """
        self.cursor.execute(f"SELECT * FROM tasks WHERE user_id='{user_id}'")
        res = self.cursor.fetchall()
        for task in res:
            print(
                f"ID: {task[0]} | User_ID: {task[1]} | Title: {task[2]} | Desc: {task[3]} "
            )
        self.authenticated_featured(user_id)


# The `if __name__ == "__main__":` statement is used to check if the current script is being run
# directly as the main module or if it is being imported as a module into another script.
if __name__ == "__main__":
    TaskManager()
