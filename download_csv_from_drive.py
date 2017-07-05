#!/usr/bin/python
from __future__ import print_function
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
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
#    source_folder_id = '0B0wfosvn2aYUQlc3OWJMQmFQNWc'
    FILENAME = 'zzhou.csv'
    SRC_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
    DST_MIMETYPE = 'text/csv'

    files = drive_service.files().list(
            q='name="%s" and mimeType="%s"' % (FILENAME, SRC_MIMETYPE),
            orderBy='modifiedTime desc,name').execute().get('files', [])
    
    if files:
        fn = '%s.csv' % os.path.splitext(files[0]['name'].replace(' ', '_'))[0]
        print('Exporting "%s" as "%s"... ' % (files[0]['name'], fn), end='')
        data = drive_service.files().export(fileId=files[0]['id'], mimeType=DST_MIMETYPE).execute()

        # if non-empty file
        if data:
            with open(fn, 'wb') as f:
                f.write(data)
            print('DONE')
if __name__ == '__main__':
    main()
