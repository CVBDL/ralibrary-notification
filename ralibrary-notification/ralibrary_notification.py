from datetime import datetime, timedelta
import dateutil.parser
import requests
import sys

# URL: https://github.com/CVBDL/RaLibraryDocs/blob/master/rest-api.md
ralibrary_borrows_api_endpoint = r'/ralibrary/api/borrows'

# URL: https://github.com/CVBDL/RaNotification
ranotification_api_endpoint = r'/ranotification/api/mailnotification'

# https certificate file path
certificate_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'assets', 'certificate.cer')

# use http basic authentication
auth = requests.auth.HTTPBasicAuth('cron', 'cron')

# timeout in seconds
timeout = 30

try:
    req = requests.get(ralibrary_borrows_api_endpoint,
                       auth=HTTPBasicAuth('user', 'pass'),
                       verify=certificate_path,
                       timeout=timeout)
    req.raise_for_status()
except TimeoutError:
    print('Timeout')
    sys.exit(1)
except HTTPError:
    print('http error.')
    sys.exit(1)
except:
    print('error')
    sys.exit(1)

#[{
#  "Borrower": "pzhong@ra.rockwell.com",
#  "BorrowTime": "2017-09-24T05:33:46.007",
#  "ExpectedReturnTime": "2017-12-23T05:33:46.007",
#  "Book": {
#    "Id": 2,
#    "Code": "P002",
#    "ISBN10": "7111348664",
#    "ISBN13": "9787111348665",
#    "Title": "???????????",
#    "Subtitle": "",
#    "Authors": "Jesse James Garrett",
#    "Publisher": null,
#    "PublishedDate": "2011",
#    "Description": null,
#    "PageCount": 191,
#    "ThumbnailLink": null,
#    "CreatedDate": "2017-12-16T18:48:51.993",
#    "RowVersion": "AAAAAAAARlI="
#  }
#}]
try:
    borrows = req.json()
except:
    print('Error parsing borrows JSON.')
    sys.exit(1)

utcnow = datetime.utcnow()

# Notify borrower two weeks before book's expire date
notification_threshold = timedelta(days=14)

for borrow in borrows:
    expected_return_time = dateutil.parser.parse(borrow['ExpectedReturnTime'])
    if utcnow + notification_threshold > expected_return_time:
        print('should notify')
    else:
        pass
