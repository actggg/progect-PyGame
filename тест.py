import sys
import os
from time import sleep
from datetime import datetime, timedelta

time = timedelta(seconds=1)
last_update = datetime.now()
money = 810
ex = 0
now = datetime.now()
print(now)
while True:
    now = datetime.now()
    if now - last_update > time:
    # update()
        last_update = now
        print(now)