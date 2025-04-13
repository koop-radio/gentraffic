from __future__ import print_function
import pickle
import os.path
import os
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def download_file(service, file_id, file_name, mime_type):
    if 'application/vnd.google-apps' in mime_type:
        request = service.files().export_media(fileId=file_id, mimeType='text/csv')
    else:
        request = service.files().get_media(fileId=file_id)
    
    fh = io.FileIO(file_name, 'wb')
    print(f"downloading {file_name} {file_id} to {os.getcwd()}")
    downloader = MediaIoBaseDownload(fh, request)
    print("downloader loaded")
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")
    print(f"File {file_name} downloaded.")

def get_most_recent_file():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Calculate the date 5 weeks ago
    five_weeks_ago = (datetime.utcnow() - timedelta(weeks=5)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Search for the most recent file containing "Traffic Log" within the last 5 weeks
    query = f"name contains 'Traffic Log' and modifiedTime > '{five_weeks_ago}'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, modifiedTime, mimeType)", orderBy="modifiedTime desc", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    files = results.get('files', [])

    if files:
        most_recent_file = files[0]
        print(f"Most recently modified file containing 'Traffic Log' within the last 5 weeks: {most_recent_file['name']}")
        print(f"File ID: {most_recent_file['id']}")
        print(f"Modified Time: {most_recent_file['modifiedTime']}")
        download_file(service, most_recent_file['id'], 'traffic.csv', most_recent_file['mimeType'])
    else:
        print("No files containing 'Traffic Log' modified within the last 5 weeks found.")

if __name__ == '__main__':
    get_most_recent_file()
