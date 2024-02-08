"""
Tutorial
https://mailtrap.io/blog/python-send-email-gmail/

Google Cloud Project
https://console.cloud.google.com/apis/credentials?authuser=2&project=iotwio


USAGE
Load service (automatically creates a service if none found).


"""

import datetime
import pickle

import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from requests import HTTPError

"""
Create OAuth service.
Don't call directly- just call load_service
"""
def create_service():
    SCOPES = [ "https://www.googleapis.com/auth/gmail.send" ]
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = discovery.build('gmail', 'v1', credentials=creds)
    return service

"""
Save OAuth service (and associated data).
Load it later with load_service().
"""
def save_session(service, data) -> None:
    with open("session.pickle","wb") as save_file:
        pickle.dump(service, save_file)
        pickle.dump(data, save_file)

"""
Load OAuth service and associated data (any type)
If no OAuth service found, create one
"""
def load_service():
    try:
        with open("session.pickle","rb") as load_file:
            service = pickle.load(load_file)
            data = pickle.load(load_file)
            return service, data
    except FileNotFoundError:
        # if there is no stored service, just make a new one and return that
        return create_service(), None

"""
Send email given an open OAuth service
Also either provide a MIMEText message or the content, recipient and subject individually.
return True if sent successfully. False otherwise.
"""
def send_email(service, message = None, body = "", recipient = None, subject = "") -> bool:
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
    service, data = load_service()

    session_count = 0
    if type(data) is int:
        session_count = data

    session_active = True
    while session_active:
        try:
            command = input("What do you want to do? >")
        except KeyboardInterrupt:
            command = 'q'

        if command[0] == 'h' or command[0] == 'H':
            print("commands: help email quit")
        elif command[0] == 'q' or command[0] == 'Q':
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

    save_session(service, session_count)
    print("quitting...")

if __name__ == "__main__":
    main()