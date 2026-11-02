#!/bin/bash
# Scrape Goodreads and sync to Firestore once. Meant to be run from cron, e.g.:
#   */5 * * * * /path/to/goodreads-scrape/run_book.sh

# Run from the repo directory so .env is found
cd "$(dirname "$0")" || exit 1

# Google application default credentials (from `gcloud auth application-default login`)
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"

/usr/bin/python3 book.py >> cron.log 2>&1
