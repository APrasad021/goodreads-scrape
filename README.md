## Usage
After cloning the repo, the dependencies will need to be installed. This can be done by running:
`
pip3 install -r requirements.txt
`
in the root directory of the repo.


After that, we'll need to create a .env file. In it, the firebase project id and goodreads user id that will be defined and used like so:

`
FIREBASE_PROJECT_ID='project-id-123'
GOODREADS_USER_ID=12345
GOODREADS_COOKIE='session-id=...; at-main=...; ...'
`

The scraper needs to be logged in to Goodreads, and Amazon (which runs Goodreads sign-in) blocks scripted password logins, so it reuses your browser's session cookie instead. To get it: log in at goodreads.com, open dev tools → Network tab, reload the page, click the first `www.goodreads.com` request, and copy the whole value of the `Cookie` request header. Paste it into `.env` in single quotes. When it expires, the scraper will stop with an error telling you to copy a fresh one.

The project id can be retrieved from Firebase console (Project Settings). The Goodreads user id is in the [profile url](https://help.goodreads.com/s/article/Where-can-I-find-my-user-ID).

Make sure that you're [authenticated as a service account](https://cloud.google.com/docs/authentication/production#create-service-account-console) in order to write to Firebase.

After those are set up correctly, you can run `python3 book.py`. This will scrape the book data for a user then write it into a books collection in Firestore. Each book's document includes its `shelf`, `shelves`, and your `rating` (0 if unrated). Books that are no longer on any of your shelves are removed from the collection.

To keep it in sync, either run `python3 main.py` (runs every minute until stopped), or schedule `run_book.sh` with cron, which runs it once and appends output to `cron.log`:

`
*/5 * * * * /path/to/goodreads-scrape/run_book.sh
`