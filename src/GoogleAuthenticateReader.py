import datetime
import time
import urllib
import urlparse

from google.cloud.client import Client
from google.cloud.storage.blob import Blob
from google.cloud.storage.bucket import Bucket


class GoogleAuthenticateReader:
    """
        GoogleAuthenticateReader can be used for generating signed URL from gs url.
    """
    def __init__(self, authenticate_file, bucket_name):
        """
            authenticate_file: GOOGLE AUTH JSON file path.
            bucket_name: Name of bucket file assocaited with.
        """
        client = Client.from_service_account_json(authenticate_file)
        self.__bucket = Bucket(client, bucket_name)

    def generate_signed_url(self, url, expiration_time=30):
        """
            url: GS url "gs://xzy/test/test.pdf"
            expiration_time: validity of signed url by default 30 mins.
        """
        u = urlparse.urlsplit(url)
        if u.scheme == 'gs':
            url = u.path[1:]
            a = Blob(url, self.__bucket)
            expiry = (datetime.datetime.now() +
                      datetime.timedelta(minutes=expiration_time)).timetuple()
            expiry = int(time.mktime(expiry))
            return a.generate_signed_url(expiry)
        else:
            return "Invalid GS url"
