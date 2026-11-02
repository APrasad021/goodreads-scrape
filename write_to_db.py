import time
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()


def write_bookshelf(books, connection):
    if not books:
        # an empty scrape almost certainly means something went wrong; don't wipe the collection
        print("{}: Scraped 0 books, skipping write".format(time.ctime()))
        return

    collection = connection.collection(u'books')
    batch = connection.batch()
    for book_key in books:
        batch.set(collection.document(book_key), books[book_key])

    # remove books that are no longer on any of the scraped shelves
    removed = [doc.id for doc in collection.list_documents()
               if doc.id != u'last_updated' and doc.id not in books]
    for book_key in removed:
        batch.delete(collection.document(book_key))

    batch.set(collection.document(u'last_updated'), {'last_updated': firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("{}: Wrote {} books to firestore, removed {}".format(time.ctime(), len(books), len(removed)))

def open_connection():
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
     'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    })

    db = firestore.client()

    return db
