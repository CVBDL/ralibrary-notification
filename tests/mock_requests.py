"""Mock requests library."""

import json as lib_json

from mock_borrows import mock_borrows


class MockResponse:
    """Mock the response"""

    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

        if json_data is None:
            self.text = None
        else:
            self.text = lib_json.dumps(json_data)

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception


def mocked_requests_get(url, **kwargs):
    return MockResponse(200, mock_borrows)

def mocked_requests_post(url, json=None, **kwargs):
    return MockResponse(200, json)
