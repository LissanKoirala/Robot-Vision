from m5stack import *
from m5ui import *
from uiflow import *
import unit

setScreenColor(0x222222)
V_0 = unit.get(unit.V_FUNCTION, unit.PORTB)


data_detail = None


face = V_0.init(V_0.FACE_DETECT)
while True:
  print((str('FaceNumber: ') + str((face.getFaceNumber()))))
  data_detail = face.getFaceDetail(1)
  print((str('Face1 value: ') + str(((str(("%.2f"%((data_detail[0] * 100)))) + str('%'))))))
  print((str('Face1 X: ') + str(data_detail[1])))
  print((str('Face1 Y: ') + str(data_detail[2])))
  print((str('Face1 W: ') + str(data_detail[3])))
  print((str('Face1 H: ') + str(data_detail[4])))
  wait_ms(2)
