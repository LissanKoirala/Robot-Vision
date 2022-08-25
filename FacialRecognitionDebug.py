from m5stack import *
from m5ui import *
from uiflow import *
import unit
import time


setScreenColor(0x222222)
V_0 = unit.get(unit.V_FUNCTION, unit.PORTB)


data_detail = None



tft = lcd

tft.font(lcd.FONT_DejaVu24, fixedwidth=False)

face = V_0.init(V_0.FACE_DETECT)
counter = 0
while True:
  counter+=30
  tft.text(0,20,(str('FaceNumber: ') + str((face.getFaceNumber()))), lcd.WHITE)
  data_detail = face.getFaceDetail(1)
  tft.text(0,40,(str('Face1 value: ') + str(((str(("%.2f"%((data_detail[0] * 100)))) + str('%'))))), lcd.WHITE)
  tft.text(0,60,(str('X: ')  + str(data_detail[1]) + str(' Y: ')  + str(data_detail[2]) + str(' W: ') + str(data_detail[3]) + str(' H: ')+ str(data_detail[4])), lcd.WHITE)
  wait(1)
  wait_ms(2)
  setScreenColor(0x222222)
