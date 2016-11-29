#!/usr/bin/env python


import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import mimetypes
from apiclient.http import MediaFileUpload


class DriveUpload:
    def __init__(self):
        pass

    def upload_file(self, flist):
        '''
        upload a file list
        '''
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        store = file.Storage('.storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('.client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store, flags) \
                    if flags else tools.run(flow, store)
        DRIVE = build('drive', 'v2', http=creds.authorize(Http()))

        FILES = []
        for f in flist:
            FILES.append((f, False))

        for filename, convert in FILES:
            metadata = {'title': filename, 'mimeType':'application/vnd.google-aps.unknown'}
            media_body = MediaFileUpload(filename, mimetype='applicaiton/vnd.google-aps.unknown')
            res = DRIVE.files().insert(convert=convert, body=metadata,
                    media_body=media_body).execute()
            if res:
                print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

