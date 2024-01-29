from post_api import *

for f in range(500,2500,200):
    print(f"freq: {f}")
    wio_post_to_buzzer(1,f)

wio_post_to_buzzer(0,0)
# Check the response
