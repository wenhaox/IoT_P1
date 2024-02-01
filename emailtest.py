"""
Tutorial
https://mailtrap.io/blog/python-send-email-gmail/

Google Cloud Project
https://console.cloud.google.com/apis/credentials?authuser=2&project=iotwio
"""

import datetime
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

def open_service():
    SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    return service


"""
send email given an open OAuth service
Also either provide a MIMEText message or the content, recipient and subject individually.
return True if sent successfully. False otherwise.
"""
def send_email(service, message = None, body = "", recipient = None, subject = ""):
    if message == None:
        if recipient == None:
            print("no email recipient specified")
            return False
        
        message = MIMEText(body)
        message['to'] = recipient
        message['subject'] = subject

    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        service.users().messages().send(userId="me", body=create_message).execute()
        print("message sent succesfully.")
        return True
    except HTTPError as error:
        print(F'error sending email: {error}')
        return False

def main():
    service = open_service()

    session_count = 0

    session_active = True
    while session_active:
        try:
            command = input("What do you want to do? >")
        except KeyboardInterrupt:
            command = 'q'

        if command[0] == 'h' or command[0] == 'H':
            print("commands: help email quit")
        elif command[0] == 'q' or command[0] == 'Q':
            print("quitting...")
            session_active = False
        elif command[0] == 'e' or command[0] == 'E':
            session_count += 1
            if session_count > 10:
                session_active = False

            to = input("recipient: ")

            if to == "test":
                to = 'trevoroblack@gmail.com'
                subject = f'Wio Test ({datetime.datetime.now().strftime("%X")}'
                body = f'test. id {session_count} - {datetime.datetime.now().strftime("%c")}'

            else:
                subject = input("subject: ")
                body = input("body: ")
        
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            send_email(service, message)
        else:
            print("That is not a valid command.")
            print("commands: help email quit")


if __name__ == "__main__":
    main()