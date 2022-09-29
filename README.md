## Usage
After cloning the repo, the dependencies will need to be installed. This can be done by running:
`
pip3 install -r requirements.txt
`
in the root directory of the repo.


After that, we'll need to create a secrets.py file. In it, the firebase project id and goodreads user id that will be defined and used like so:

`
FIREBASE_PROJECT_ID = 'project-id-123'
GOODREADS_USER_ID = 12345
`

The project id can be retrieved from Firebase console (Project Settings).

Make sure that you're [authenticated as a service account](https://cloud.google.com/docs/authentication/production#create-service-account-console) in order to write to Firebase.

After those are set up correctly, you can run `python3 book.py`. This will scrape the book data for a user then write it into a books collection in Firestore.

*TODO:*

[ ]: Save user ratings of books

[ ]: Get picture of book cover