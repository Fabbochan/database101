import sqlite3
from faker import Faker
from datetime import datetime
import random


def create_user(username, password):
    """
    This function creates a new user in the SQLITE3 DB with the passed credentials
    """

    # database gets opened and a cursor is created
    enabled = True

    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    # with the recieved data a new user gets created in the users table
    cursor.execute("""INSERT INTO users(username, enabled)
                    VALUES(?,?)""", (username, enabled))

    db.commit()

    db.close()

    # status print
    print("STATUS: User created.")