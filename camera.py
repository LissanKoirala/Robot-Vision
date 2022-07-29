import image
import sensor
import time
from m5stack import *


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

while True:
  img = sensor.snapshot()
  lcd.display(img)
