import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")


class GoodreadsLoginError(Exception):
    pass


def get_session():
    """Return a requests session logged in with the browser cookie in GOODREADS_COOKIE."""
    cookie = os.getenv('GOODREADS_COOKIE')
    if not cookie:
        raise GoodreadsLoginError('GOODREADS_COOKIE must be set in .env (see README)')

    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Cookie'] = cookie.strip()
    # Goodreads is occasionally slow; retry timeouts and 5xx errors with backoff
    retries = Retry(total=4, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def check_logged_in(response):
    if '/user/sign_in' in response.url or '/ap/signin' in response.url:
        raise GoodreadsLoginError(
            'Goodreads redirected to sign-in: GOODREADS_COOKIE has expired or is wrong. '
            'Copy a fresh one from your browser into .env (see README).')
