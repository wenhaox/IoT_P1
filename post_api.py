import time

import requests
import json

# The URL you're sending the request to
def wio_post(url):
    print(f"posting to {url}...")
    response = requests.post(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    return response.status_code,response.text

url = 'https://cn.wio.seeed.io/v1/node/GenericPWMOutD0/pwm/{}?access_token=07042fa3919ad945a5e9384e1a130789'

# duty_percent: 0-100
# freq: 1000-2000
def wio_post_to_buzzer(duty_percent,freq):
    url = f"https://cn.wio.seeed.io/v1/node/GenericPWMOutD0/pwm_with_freq/{duty_percent}/{freq}?access_token=07042fa3919ad945a5e9384e1a130789"
    return wio_post(url)

def wio_post_to_led(status):
    url = f"https://cn.wio.seeed.io/v1/node/GenericDOutD0/onoff/{status}]?access_token=dd6c0019eb310b68c79dea774e6e1972"
    
    return wio_post(url)

# status: 0 or 1
def wio_post_to_relay(status):
    url = f"https://cn.wio.seeed.io/v1/node/GroveRelayD1/onoff/{status}?access_token=dd6c0019eb310b68c79dea774e6e1972"
    
    return wio_post(url)


