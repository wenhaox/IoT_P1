from post_api import *
from read_api import *

wio_post_to_relay(0)
try:
    while True:
        response = read_sensor('https://cn.wio.seeed.io/v1/node/GroveMoistureA0/moisture?access_token=dd6c0019eb310b68c79dea774e6e1972')
        sensor_data = json.loads(response.decode('utf-8'))["moisture"]
        sensor_data = int(sensor_data)
        print(sensor_data)
        if sensor_data < 30:
             wio_post_to_relay(1)
        else:
             wio_post_to_relay(0)


except KeyboardInterrupt:
    print("Stopped by User")