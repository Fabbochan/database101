import sqlite3
from faker import Faker
from datetime import datetime
import random


# def create_user(username, enabled, street, city, state):
#     """
#     This function creates a new user in the SQLITE3 DB with the passed credentials
#     """
#
#     # database gets opened and a cursor is created
#     db = sqlite3.connect("db.sqlite3")
#     cursor = db.cursor()
#
#     # with the recieved data a new user gets created in the users table
#     cursor.execute("""INSERT INTO users(username, enabled)
#                     VALUES(?,?)""", (username, enabled))
#
#     db.commit()
#
#     # we access the new user_id
#     cursor.execute("""SELECT id FROM users WHERE username=?""", (username,))
#     user = cursor.fetchone()
#     # and store the user_id in the user_id variable
#     user_id = list(user)[0]
#
#     # we populate the addresses table with the new user information and connect it to the user_id
#     cursor.execute("""INSERT INTO addresses(user_id, street, city, state) VALUES(?,?,?,?)""",
#                    (user_id, street, city, state))
#     db.commit()
#
#     # database gets closed
#     db.close()
#
#     # status print
#     print("STATUS: User created.")/


def create_user(username, password):
    """
    This function creates a new user in the SQLITE3 DB with the passed credentials
    """

    # database gets opened and a cursor is created
    enabled = True

    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    # with the recieved data a new user gets created in the users table
    cursor.execute("""INSERT INTO users(username, enabled, password)
                    VALUES(?,?,?)""", (username, enabled, password,))

    db.commit()

    db.close()

    # status print
    print("STATUS: User created.")


def create_book_review(reviewer_name, content, rating, published_date):
    book_id = 1
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO reviews(book_id, reviewer_name, content, rating, published_date)
                        VALUES(?,?,?,?,?)""", (book_id, reviewer_name, content, rating, published_date))
    db.commit()
    db.close()
    print("Book Review created!")


def book_checkout(book_id, username, return_date):
    """
    This function recievs a required book_id, a username and a return date
    The function checks if the username exists in the users table
    If the user exists, user info gets extracted and stored into the checkout table
    If the user does not exist, the function prints a "Checkout failed"
    """

    # database gets opened and a cursor is created
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    # users table gets search for recieved username
    cursor.execute("""SELECT id, username, enabled FROM users WHERE username=?""", (username,))
    user = cursor.fetchone()

    # validity check if user exists and is enabled
    if user and user[2]:

        # to get the current time for the checkout
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y-%H:%M:%S")
        # user info required for the checkout table
        user_id = user[0]
        checkout_time = current_time
        return_date = return_date
        book_id = book_id

        # insertion of the user info
        cursor.execute("""INSERT INTO checkouts(user_id, book_id, checkout_date, return_date)
                        VALUES(?,?,?,?)""", (user_id, book_id, checkout_time, return_date))
        db.commit()
        print("STATUS: Checkout successful")

    # if criteria is not met, functions will return a "checkout fail"
    else:
        print("STATUS: Checkout failed")

    # database gets closed
    db.close()


def pick_book_id():
    """
    This function picks a random book from the books table
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    cursor.execute("""SELECT id FROM books""")
    # we get a tuple back and store it in fetched_book_ids
    fetched_book_ids = cursor.fetchall()

    # we create a list called book_ids and append the tuple objects to the list
    book_ids = []
    for book_id in fetched_book_ids:
        book_ids.append(list(book_id)[0])

    db.close()

    # we return the book_ids list
    return book_ids


def pick_book():
    """
    This function picks a random book from the books table
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    cursor.execute("""SELECT * FROM books""")
    # we get a tuple back and store it in fetched_book_ids
    fetched_books = cursor.fetchall()

    # we create a list called book_ids and append the tuple objects to the list
    book_info = []
    for info in fetched_books:
        book_info.append(list(info))

    db.close()

    # we return the book_ids list
    return book_info


def pick_user():
    """
    With this function we want to pick a random user
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    # Here we fetch all the user from the users table
    cursor.execute("""SELECT username FROM users""")
    fetched_usernames = cursor.fetchall()

    # we create an empty list to store the users into
    usernames = []

    # we convert the user tuples and store them in the usernames list
    for username in fetched_usernames:
        usernames.append(list(username)[0])

    # we pick one random user name from the users list
    username_number = random.randint(0, len(usernames) - 1)
    username = usernames[username_number]

    return username


def review_book(book_id, username, content, rating, published_date):
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    # Here we insert the recieved data into the reviews table
    cursor.execute("""INSERT INTO reviews(book_id, reviewer_name, content, rating, published_date) 
                    VALUES(?,?,?,?,?)""",
                   (book_id, username, content, rating, published_date))
    db.commit()
    db.close()

    print("STATUS: Review created.")


def check_user(username):
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("""SELECT id, username, enabled, password FROM users WHERE username=?""", (username,))
    user = list(cursor.fetchone())
    db.close()
    return user


def login_user(username):
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("""SELECT id, username, enabled FROM users WHERE username=?""", (username,))
    user = list(cursor.fetchone())

    # to get the current time for the checkout
    now = datetime.now()
    current_time = now.strftime("%d_%m_%Y-%H:%M:%S")

    cursor.execute("""INSERT INTO login(user_id, login_time) VALUES(?,?)""", (user[0], current_time))
    db.commit()
    db.close()
    return user


def fetch_all_user():
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM users """)
    fetched_user = list(cursor.fetchall())
    db.close()
    return fetched_user


def fetch_all_reviews():
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM reviews """)
    fetched_reviews = list(cursor.fetchall())
    db.close()
    return fetched_reviews


if __name__ == "__main__":

    # fake data
    faker = Faker()
    # name = faker.name()
    # enabled = "t"
    # city = faker.city()
    # street = faker.street_address()
    # state = faker.country_code()
    # content = faker.text()
    # rating = random.randint(1,5)
    # published_date = faker.date_time_this_century()

    # create_user(username=name, enabled=enabled, street=street, city=city, state=state)

    # here we create a random book id from the books table
    # num_books = pick_book()
    # book_id = random.randint(0, len(num_books)-1)
    # book_checkout(book_id=book_id, username="Christopher Lopez", return_date="30.04.2022")

    # book_ids = pick_book()
    # book_id = random.randint(0, len(book_ids)-1)
    # username = pick_user()
    # review_book(book_id, username=username, content=content, rating=rating, published_date=published_date)

