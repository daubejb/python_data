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
    
    for filename in os.listdir("/home/jedaube/scratch/tests"):
        file_metadata = {
                'name' : filename,
                'mimeType' : 'application/vnd.google-apps.spreadsheet'
                }
        media = MediaFileUpload('/home/jedaube/scratch/tests/jedaube.csv',
                mimetype='text/csv',
                resumable=True)
        file = drive_service.files().create(body=file_metadata,
                media_body=media,
                fields='id').execute()
        time.sleep(1)

#        file_metadata = {
#                'name' : 'jedaube.csv',
#                'mimeType' : 'application/vnd.google-apps.spreadsheet'
#                }
#        media = MediaFileUpload('/home/jedaube/scratch/tests/jedaube.csv',
#                mimetype='text/csv',
#                resumable=False)
#        file = drive_service.files().create(body=file_metadata,
#                media_body=media,
#                fields='id').execute()
if __name__ == '__main__':
    main()
