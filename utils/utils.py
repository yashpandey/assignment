import requests
import time
import json
from collections import defaultdict
import pytest
from utils import auth

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.fixture(scope='module')
def user_data():
    with open('config.json', 'r') as f:
        return json.load(f)


def get(resource, params=None, expected_status_code=200, user=user_data):
    response = call(requests.get, resource, expected_status_code, user, params=params)
    return defaultdict(lambda: None, response.json())


def post(resource, params=None, payload=None, expected_status_code=201, user=user_data):
    if payload is None:
        payload = {}

    response = call(requests.post, resource, expected_status_code, user, data=json.dumps(payload), params=params)
    return defaultdict(lambda: None, response.json())


def patch(resource, params=None, payload=None, expected_status_code=200, user=user_data):
    if payload is None:
        payload = {}
    call(requests.patch, resource, expected_status_code, user, data=json.dumps(payload), params=params)


def put(resource, params=None, payload=None, expected_status_code=200, user=None):
    if payload is None:
        payload = {}

    response = call(requests.put, resource, expected_status_code, user, data=json.dumps(payload), params=params)
    return defaultdict(lambda: None, response.json())


def delete(resource, params=None, expected_status_code=204, user=user_data):
    """
    This is a HTTP DELETE method to delete a resource from the system
    :param resource: Resource you want to delete
    :param params: params along with the HTTP call
    :param expected_status_code: expected HTTP status code
    :param user: access token
    """
    return call(requests.delete, resource, expected_status_code, user, params=params)


def call(request_method, resource, expected_status_code, user, headers=None, data=None, params=None):
    url = "{}".format(resource)
    if headers is None:
        headers = {}

    headers['accept'] = "application/json"

    headers['token'] = auth.get_token(
        username=user.get('user').get('name'), password=user.get('user').get('password'),force_refresh=False)

    response = request_method(url, params=params, headers=headers, data=data)

    if response.status_code == 401:
        # Retry with a new token
        headers['token'] = auth.get_token(username=user.username, password=user.password, force_refresh=False)
        response = request_method(url, params=params, headers=headers, data=data)

    message = "Got status code: {}, expected: {}, response body: {}".format(
        response.status_code, expected_status_code, response.text)
    assert response.status_code == expected_status_code, message

    return response


def wait_until(some_predicate, timeout, period=1, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        if some_predicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False
