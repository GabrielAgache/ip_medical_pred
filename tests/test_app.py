import sys
# import app
from flask import request
sys.path.append('..')


def test_root(test_client):
    response = test_client.get('/')
    assert response.data == b'Hello from flask'
