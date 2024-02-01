import requests
import smtplib
import ssl
import time
import urllib.request

def read_sensor(api_url):
    # Create an unverified SSL context
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(api_url, context=context)
    data = response.read()
    return data

def control_output(api_url, command):
    response = requests.post(api_url, data={'command': command})
    return response.status_code

def send_email(subject, message, sender_email, receiver_email, smtp_server, port, login, password):
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, f'Subject: {subject}\n\n{message}')

# control_output('your_output_api_url', '1')  # Turn on a device
# send_email('Alert', 'Sensor triggered', 'your_email@gmail.com', 'receiver_email@gmail.com', 'smtp.gmail.com', 587, 'your_email@gmail.com', 'your_password')
