from datetime import datetime, timedelta


mock_borrows = [
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2017-09-24T11:08:48",
    # today
    "ExpectedReturnTime": "2018-01-05T00:00:00",
    "Book": {
      "Id": 1,
      "Code": "P001",
      "ISBN10": "0596008031",
      "ISBN13": "9780596008031",
      "Title": "Designing Interfaces",
      "Subtitle": "Patterns for Effective Interaction Design",
      "Authors": "Jenifer Tidwell",
      "Publisher": "\"O'Reilly Media, Inc.\"",
      "PublishedDate": "2005-11-21",
      "Description": "",
      "PageCount": 331,
      "ThumbnailLink": "",
      "CreatedDate": "2017-12-20T08:13:12.837"
    }
  },
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2018-02-01T05:19:43.957",
    # 14 days after today
    "ExpectedReturnTime": "2018-01-19T00:00:00",
    "Book": {
      "Id": 6,
      "Code": "P006",
      "ISBN10": "0596554478",
      "ISBN13": "9780596554477",
      "Title": "JavaScript: The Definitive Guide",
      "Subtitle": "The Definitive Guide",
      "Authors": "David Flanagan",
      "Publisher": "\"O'Reilly Media, Inc.\"",
      "PublishedDate": "2006-08-17",
      "Description": "",
      "PageCount": 1032,
      "ThumbnailLink": "",
      "CreatedDate": "2017-12-20T08:13:12.837"
    }
  },
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2018-02-01T05:19:43.957",
    # most later time
    "ExpectedReturnTime": "2018-11-11T05:19:43.957",
    "Book": {
      "Id": 5,
      "Code": "P005",
      "ISBN10": "0596554877",
      "ISBN13": "9780596554873",
      "Title": "JavaScript: The Good Parts",
      "Subtitle": "The Good Parts",
      "Authors": "Douglas Crockford",
      "Publisher": "\"O'Reilly Media, Inc.\"",
      "PublishedDate": "2008-05-08",
      "Description": "Most programming languages contain good and bad parts, but...",
      "PageCount": 172,
      "ThumbnailLink": "",
      "CreatedDate": "2017-12-20T08:13:12.837"
    }
  },
  {
    "Borrower": "patrick@example.com",
    "BorrowTime": "2018-02-01T05:19:43.957",
    # long time ago
    "ExpectedReturnTime": "2017-11-11T05:19:43.957",
    "Book": {
      "Id": 52,
      "Code": "P410",
      "ISBN10": None,
      "ISBN13": "9781491946008",
      "Title": "Fluent Python",
      "Subtitle": "",
      "Authors": "Luciano Ramalho",
      "Publisher": "O'Reilly Media",
      "PublishedDate": "2015-8-20",
      "Description": "",
      "PageCount": 768,
      "ThumbnailLink": "",
      "CreatedDate": "2017-11-09T00:42:00.177"
    }
  }
]

def make_borrow(days_ago=0):
    expected_return_time = (
        datetime.utcnow() - timedelta(days=days_ago)).isoformat()

    return {
        "Borrower": "patrick@example.com",
        "BorrowTime": "2018-02-01T05:19:43.957",
        "ExpectedReturnTime": expected_return_time,
        "Book": {
          "Id": 52,
          "Code": "P410",
          "ISBN10": None,
          "ISBN13": "9781491946008",
          "Title": "Fluent Python",
          "Subtitle": "",
          "Authors": "Luciano Ramalho",
          "Publisher": "O'Reilly Media",
          "PublishedDate": "2015-8-20",
          "Description": "",
          "PageCount": 768,
          "ThumbnailLink": "",
          "CreatedDate": "2017-11-09T00:42:00.177"
        }
    }
