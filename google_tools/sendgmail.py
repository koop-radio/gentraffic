from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request  # Ensure this is added
import base64
import os

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def sendgmail(subject, body, to="playout@koop.org"):
    # Email configuration
    sender_email = "prodmmauto@koop.org"
    receiver_email = to
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(sender_email, receiver_email, subject, body)
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print("Email sent successfully!")
    except HttpError as error:
        print(f'An error occurred: {error}')

# Example usage

if __name__ == '__main__':
    subject = "A test from prodmm"
    body = "somebody"
    to = "sendjunk4me@gmail.com"
    sendgmail(subject, body, to)

