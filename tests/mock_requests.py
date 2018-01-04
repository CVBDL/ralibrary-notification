"""Mock requests library."""

import json as lib_json


mock_borrows = [
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2017-09-24T11:08:48",
    "ExpectedReturnTime": "2017-10-24T11:08:48",
    "Book": {
      "Id": 2,
      "Code": "P002",
      "ISBN10": "7111348664",
      "ISBN13": "9787111348665",
      "Title": "???????????",
      "Subtitle": "",
      "Authors": "Jesse James Garrett",
      "Publisher": None,
      "PublishedDate": "2011",
      "Description": None,
      "PageCount": 191,
      "ThumbnailLink": None,
      "CreatedDate": "2017-09-24T11:08:48.93"
    }
  },
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2017-09-24T05:19:43.957",
    "ExpectedReturnTime": "2017-12-23T05:19:43.957",
    "Book": {
      "Id": 4,
      "Code": "P004",
      "ISBN10": "7513902062",
      "ISBN13": "9787513902069",
      "Title": "????????",
      "Subtitle": "",
      "Authors": "William Strunk, Jr.",
      "Publisher": "????????",
      "PublishedDate": "2013",
      "Description": "?????????????????????????????????. ????????, ??????(???????????)????(???????????)?18????????????, ?????????????????????????.",
      "PageCount": 187,
      "ThumbnailLink": None,
      "CreatedDate": "2017-09-24T11:08:48.93"
    }
  }
]


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
