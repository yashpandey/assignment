import json
import requests
import pytest
from multiprocessing import Lock

lock = Lock()


@pytest.fixture(scope='module')
def user_data():
    with open('config.json', 'r') as f:
        return json.load(f)


def get_token(username,
              password, force_refresh):
    """
    Gets an auth token, either for a specified or default user.
    Tokens are cached per-username, but a new token can be force-retrieved if force_refresh=True.
    """
    tokens = {}
    if not tokens:
        # We only need one thread to get the token
        lock.acquire()

        try:
            # Check one more time to see if another thread already got the token
            if not tokens:
                token = _authenticate(username, password, user_data)
                tokens[username] = token
        finally:
            lock.release()
    elif force_refresh:
        token = _authenticate(username, password)
        tokens[username] = token

    return tokens[username]


def _authenticate(username, password, user_data):
    request_body = {
        "auth": {
            "passwordCredentials": {
                "username": username,
                "password": password
            }
        }
    }

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json'
    }

    r = requests.post('{}'.format(user_data.get("auth_url")),
                      data=json.dumps(request_body), headers=headers)

    if r.status_code == 200:
        token = r.json()[u'access'][u'token'][u'id']
    else:
        raise RuntimeError("Unable to auth with credentials provided, HTTP status code: {0}, "
                           "and reason {1}".format(r.status_code, r.text))

    return token
