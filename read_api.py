import ssl
import urllib.request

# Function to read the sensor data from the API 
def read_sensor(api_url):
    # Create an unverified SSL context
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(api_url, context=context)
    data = response.read()
    return data