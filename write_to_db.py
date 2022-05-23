import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from secrets import FIREBASE_PROJECT_ID


def write_bookshelf(books, connection):
    batch = connection.batch()
    for book_key in books:
        book_ref = connection.collection(u'books').document(book_key)
        batch.set(book_ref, books[book_key]) 
    batch.commit()

def open_connection():
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
     'projectId': FIREBASE_PROJECT_ID,
    })

    db = firestore.client()

    return db
