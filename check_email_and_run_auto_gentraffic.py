from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auto_gentraffic import auto_gentraffic
import os

# Import your sendgmail function from its module
from google_tools.sendgmail import sendgmail

def get_gmail_service(token_file_name, scopes):
    creds = None
    # Load credentials from the file
    if os.path.exists(token_file_name):
        creds = Credentials.from_authorized_user_file(token_file_name, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file_name, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def check_email_and_run_auto_gentraffic(service):
    try:
        # Search for unread emails with the subject "UPDATE"
        query = 'is:unread subject:UPDATE'
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])
        print("\n\nmessages are:\n\n",messages)

        if not messages:
            print("No messages found. No update was run.")
            return

        print(f"Found {len(messages)} unread 'UPDATE' messages.")
        for message in messages:
            # Mark the email as read
            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

        # Simulate running auto_gentraffic and send a notification
        auto_gentraffic() # Uncomment and use your actual function call
        print("auto_gentraffic executed successfully")

    except HttpError as error:
        print(f'An error occurred: {error}')
        sendgmail("Error: Program Execution Failed", f"An error occurred while executing the program:\n\n{error}", sender_email)

if __name__ == '__main__':
    sender_email = "your_email@gmail.com"  # Update with the actual sender's email
    scopes = ['https://www.googleapis.com/auth/gmail.modify']
    token_file_name = 'check_email_token.json'  # A new token file name for this specific scope and usage
    service = get_gmail_service(token_file_name, scopes)
    check_email_and_run_auto_gentraffic(service)

