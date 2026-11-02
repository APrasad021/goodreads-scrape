import os
from dotenv import load_dotenv
from goodreads_auth import get_session
from get_profile_books import SHELVES, get_bookshelf
from write_to_db import open_connection, write_bookshelf

load_dotenv()
# comment out the following line if you don't want to write to the database
connection = open_connection()


def main():
    book_data = {}
    session = get_session()

    for shelf in SHELVES:
        book_data.update(get_bookshelf(os.getenv('GOODREADS_USER_ID'), shelf, session))

    # comment out the following line if you don't want to write to the database
    write_bookshelf(book_data, connection)


main()
