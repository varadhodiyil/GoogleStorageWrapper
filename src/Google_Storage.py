import argparse
import json
import os

from googleapiclient import discovery, http
from oauth2client.client import GoogleCredentials, flow_from_clientsecrets
from oauth2client.service_account import ServiceAccountCredentials


class GoogleStorage:
    def __init__(self, bucket_name, credentials_path):
        self.BUCKET_NAME = bucket_name
        self.CREDENTIALS_JSON = credentials_path

    def setBucketName(self, bucket):
        self.BUCKET_NAME = bucket
	
	def setCredentialsPath(self, credentials_path):
		self.CREDENTIALS_JSON = credentials_path

    def create_service(self):
        # Get the application default credentials. When running locally, these are
        # available after running `gcloud init`. When running on compute
        # engine, these are available from the environment.
        #credentials = GoogleCredentials.get_application_default()
        # Construct the service object for interacting with the Cloud Storage API -
        # the 'storage' service, at version 'v1'.
        # You can browse other available api services and versions here:
        #     http://g.co/dev/api-client-library/python/apis/
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_JSON)
        #credentials = flow_from_clientsecrets('google-services.json')
        return discovery.build('storage', 'v1', credentials=credentials)

    def upload_object(self, filename, readers=[], predefinedAcl='authenticatedRead', owners=[], name=None):
        service = self.create_service()
        # This is the request body as specified:
        # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
        if not name:
            name = filename
        body = {
            'name': name,
            'predefinedAcl': predefinedAcl,
            'projection': 'full',
            'uploadType': 'media',
        }

        # If specified, create the access control objects and add them to the
        # request body

        if readers or owners:
            body['acl'] = []

        for r in readers:
            body['acl'].append({
                'entity': 'user-%s' % r,
                'role': 'READER',
                'name': r
            })

        for o in owners:
            body['acl'].append({
                'entity': 'user-%s' % o,
                'role': 'OWNER',
                'email': o
            })
        # Now insert them into the specified bucket as a media insertion.

        # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert
        with open(filename, 'rb') as f:
            req = service.objects().insert(name=name, predefinedAcl=predefinedAcl,
                                           bucket=self.BUCKET_NAME, media_body=http.MediaIoBaseUpload(f, 'application/octet-stream'))
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            resp = req.execute()
        return resp['mediaLink']

    def get_bucket_metadata(self):
        """Retrieves metadata about the given bucket."""
        service = self.create_service()
        # Make a request to buckets.get to retrieve a list of objects in the
        # specified bucket.
        req = service.buckets().get(bucket=self.BUCKET_NAME)
        return req.execute()

    def create_bucket(self, project_id):
        service = self.create_service()
        # Make a request to buckets.get to retrieve a list of objects in the
        # specified bucket.
        body = {
            'name': self.BUCKET_NAME,
            'predefinedAcl': 'publicRead',
            'projection': 'full',
            'projection': 'full',
            'predefinedDefaultObjectAcl': 'publicRead',
            'projection': 'full'

        }
        req = service.buckets().insert(project=project_id, body=body)
        return req.execute()

    def list_bucket(self):
        """Returns a list of metadata of the objects within the given bucket."""
        service = self.create_service()
        # Create a request to objects.list to retrieve a list of objects.
        fields_to_return = \
            'nextPageToken,items(name,size,contentType,metadata(my-key))'
        req = service.objects().list(bucket=self.BUCKET_NAME, fields=fields_to_return)
        all_objects = []
        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.
        while req:
            resp = req.execute()
            all_objects.extend(resp.get('items', []))
            req = service.objects().list_next(req, resp)
        return all_objects

    def get_object(self, filename, out_file):
        service = self.create_service()
        # Use get_media instead of get to get the actual contents of the object.
        # http://g.co/dev/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
        req = service.objects().get_media(bucket=self.BUCKET_NAME, object=filename)
        downloader = http.MediaIoBaseDownload(out_file, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download {}%.".format(int(status.progress() * 100)))
        return out_file

    def delete_object(self, filename):
        service = self.create_service()
        req = service.objects().delete(bucket=self.BUCKET_NAME, object=filename)
        resp = req.execute()
        return resp
