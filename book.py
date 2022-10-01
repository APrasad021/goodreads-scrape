import os
from dotenv import load_dotenv
from get_profile_books import SHELVES, get_bookshelf
from write_to_db import open_connection, write_bookshelf

load_dotenv()

def main():
    book_data = {}

    for shelf in SHELVES:
        book_data.update(get_bookshelf(os.getenv('GOODREADS_USER_ID'), shelf))

    ## comment out the following 2 lines if you don't want to write to the database
    connection = open_connection()
    write_bookshelf(book_data, connection)

main()