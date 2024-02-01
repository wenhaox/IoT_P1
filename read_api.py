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

try:
    while True:
        sensor_data = read_sensor('https://cn.wio.seeed.io/v1/node/GroveMoistureA0/moisture?access_token=f1f49eed4514a203662fb715e9d10510')
        print(sensor_data)
        if(sensor_data>30):
            send_email('test','Moisture is '+ sensor_data,'iotjhu@gmail.com','iotjhu@gmail.com','smtp.gmail.com',465,'iotjhu@gmail.com','135qwe!!')
        time.sleep(1)  # Delay for 1 second to avoid too many requests
        

except KeyboardInterrupt:
    print("Stopped by User")

# control_output('your_output_api_url', '1')  # Turn on a device
# send_email('Alert', 'Sensor triggered', 'your_email@gmail.com', 'receiver_email@gmail.com', 'smtp.gmail.com', 587, 'your_email@gmail.com', 'your_password')
