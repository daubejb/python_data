#!/usr/bin/python
from __future__ import print_function
import httplib2
import os
import time
import io

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from io import FileIO
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MojoContentCleanUp'


def get_credentials():
    #Gets valid user credentials from storage.

    #If nothing has been stored, or if the stored credentials are invalid,
    #the OAuth2 flow is completed to obtain the new credentials.

    #Returns:
    #    Credentials, the obtained credential.

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'MojoContentCleanUp-cfc2596e800f.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('MojoContentCleanUp-cfc2596e800f.json',
                SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)
    run_date_time = time.strftime("%Y-%m-%d")
    destination_folder_name = 'Stale Mojo Content ' + run_date_time
    page_token = None
    count = 0
    ids_to_download = []
    while True:
        response = drive_service.files().list(q="'0B0wfosvn2aYUQlc3OWJMQmFQNWc' in parents",
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name)',
                                         pageToken=page_token).execute()
        for file in response.get('files', []):
            time.sleep(.25)
            # Process change
            request = drive_service.files().export_media(fileId=file.get('id'),
                    mimeType='text/csv')
            download = "download/" + file.get('name')
            fh = io.FileIO(download, mode='wb')
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            print(" %s " % (file.get('name')))
            count += 1
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;
        print(count)
    print(count)
    print(ids_to_download)

if __name__ == '__main__':
    main()
