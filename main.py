from post_api import *
from read_api import *
from email_api import *

import time
import json

EMAIL_REC = "iotjhu@gmail.com"

def main():
    water_state = False
    wio_post_to_relay(0)
    
    service, data = load_service()
    try:
        while True:
            time.sleep(5)
            response = read_sensor('https://cn.wio.seeed.io/v1/node/GroveMoistureA0/moisture?access_token=dd6c0019eb310b68c79dea774e6e1972')
            sensor_data = json.loads(response.decode('utf-8'))["moisture"]
            sensor_data = int(sensor_data)
            print(sensor_data)
            if sensor_data < 30:
                wio_post_to_relay(1)
                if water_state is False:
                    # state was changed - send email once
                    send_email(service, body="Your plant is being watered.", recipient=EMAIL_REC, subject="WIO Plant Waterer (needs attention)")
                    water_state = True

            else:
                wio_post_to_relay(0)
                if water_state is True:
                    # state was changed - send email once
                    send_email(service, body="Your plant is now watered.", recipient=EMAIL_REC, subject="WIO Plant Waterer (watered)")
                    water_state = False

    except KeyboardInterrupt:
        print("Stopped by User")
        save_session(service, data)

if __name__ == "__main__":
    main()