import time
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()


def write_bookshelf(books, connection):
    batch = connection.batch()
    for book_key in books:
        book_ref = connection.collection(u'books').document(book_key)
        batch.set(book_ref, books[book_key])
    connection.collection(u'books').document(u'last_updated').set({'last_updated': firestore.SERVER_TIMESTAMP})
    batch.commit()
    print("{}: Wrote {} books to firestore".format(time.ctime(), len(books)))

def open_connection():
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
     'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    })

    db = firestore.client()

    return db
