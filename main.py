# As of 28/3/20
# BluBot Head Servo control software
# by L Villazon
# released into the public domain
# https://m5stack.com/products/servo-module
# https://github.com/m5stack/M5Stack_MicroPython

# REFERENCE WEBSITES
# https://github.com/m5stack/UIFlow-Code/wiki/Display
# https://docs.python.org/3/tutorial/classes.html
# https://www.tutorialspoint.com/python/python_lists.htm
# <-- max line length to comply with PEP-8 (79 chars) ------------------------->
from m5stack import *
import i2c_bus
import math
SERVO_ENABLE = False # set to false to disable servos for testing
# initialise i2c bus
i2c = i2c_bus.easyI2C((21, 22), 0x53)
class Head:
    nodRestAngle = 0
    tiltRestAngle = 0
    twistRestAngle = 0
    jawRestAngle = 0
    nodCurrentAngle = 0
    tiltCurrentAngle = 0
    twistCurrentAngle = 0
    jawCurrentAngle = 0
    axes = ['twist', 'nod', 'tilt', 'jaw']
    activeAxis = 'twist'
    def setNextAxis(self):
        self.activeAxis = self.axes[(self.axes.index(self.activeAxis) + 1) 
                                     % len(self.axes)]
    def setServo(self, channel, angle):
        # the 0x10 tells the write function to use pwm to drive the servo to the
        # specified angle
        if SERVO_ENABLE == True:
            i2c.write_u8(channel + 0x10, angle)
    def moveActiveAxis(self, angleChange):
        # increment the currently active axis
        if self.activeAxis == self.axes[0]:
            self.twist(self.twistCurrentAngle + angleChange)
        elif self.activeAxis == self.axes[1]:
            self.nod(self.nodCurrentAngle + angleChange)
        elif self.activeAxis == self.axes[2]:
            self.tilt(self.tiltCurrentAngle + angleChange)
        elif self.activeAxis == self.axes[3]:
            self.moveJaw(self.jawCurrentAngle + angleChange)
    def nod(self, angle):
        # tilt the head forward and back
        # (not implemented yet)
        self.nodCurrentAngle = angle
    def tilt(self, angle):
        # tilt the head from side to side
        # (not implemented yet)
        self.tiltCurrentAngle = angle
    def twist(self, angle):
        # twist the head left and right
        # TODO: check constraints
        self.twistCurrentAngle = angle
        self.setServo(0, angle)
    def moveJaw(self, angle):
        # move the jaw opena and shut
        # (not implemented yet)
        self.jawCurrentAngle = angle
    def moveEyes(self, angle):
        # look left and right
        # (not implemented yet)
        pass
    def __init__(self):
        self.nod(self.nodRestAngle)
        self.tilt(self.tiltRestAngle)
        self.twist(self.twistRestAngle)
        self.moveJaw(self.jawRestAngle)
    def getColour(self, axis):
        if axis == self.activeAxis:
            return lcd.CYAN
        else:
            return lcd.DARKCYAN
    def _draw(self, visible=True):
        # 3D rotation headache!
        https://math.stackexchange.com/questions/2004800/math-for-simple-3d-coordinate-rotation-python
        

        # graphical representation of the head angle/pose
        # currently just 3 ellipses to represent the outline, equator & meridian
        CX = 0 # centre X, Y for all ellipses - never changes
        CY = 0
        # absolute head dimensions
        # these are used as the basis for the ellipses, 
        # modified by twist & tilt
        WIDTH = 80      
        HEIGHT = 100
        # coords of the 'nose' ie the notional origin point of the face
        noseX = int(
                noseX * math.cos(math.radians(self.twistCurrentAngle)) -
                noseY * math.sin(math.radians(self.twistCurrentAngle))
                )
        noseY = int(
                noseX * math.sin(math.radians(self.twistCurrentAngle)) -
                noseY * math.cos(math.radians(self.twistCurrentAngle))
                )
        # outline width - never changes
        radiusX = WIDTH
        # outline height - changes when nodding         
        radiusY = 100
        # meridian width - changes when twisting
        radiusTwistX = max(3,
                           int(WIDTH * 
                           math.sin(math.radians(
                           abs(self.twistCurrentAngle)))))
        # equator height - changes when nodding
        radiusNodY = max(3,
                          int(WIDTH *
                          math.sin(math.radians(
                          abs(self.nodCurrentAngle)))))
        
        # choose which ellipse segments are visible due to tilt & twist
        # when nodding upwards, the top half of the ellipse is visible
        # when nodding downwards, this switches to the bottom half
        # a similar thing happens for left and right for the twist
        UPPER_RIGHT_SEGMENT = 1
        UPPER_LEFT_SEGMENT  = 2
        LOWER_LEFT_SEGMENT  = 4
        LOWER_RIGHT_SEGMENT = 8
        if self.twistCurrentAngle > 0:
            twistSegments = UPPER_RIGHT_SEGMENT + LOWER_RIGHT_SEGMENT
        else:
            twistSegments = UPPER_LEFT_SEGMENT + LOWER_LEFT_SEGMENT
        if self.nodCurrentAngle > 0:
            nodSegments = LOWER_LEFT_SEGMENT + LOWER_RIGHT_SEGMENT
        else:
            nodSegments = UPPER_LEFT_SEGMENT + UPPER_RIGHT_SEGMENT
        
        # select whether to draw or erase the head
        if visible:
            lcd.circle(noseX, noseY, 5, lcd.RED, lcd.RED)
            lcd.ellipse(CX, CY, radiusX, radiusY, color=lcd.DARKCYAN)
            lcd.ellipse(CX, CY, radiusTwistX, radiusY,
                        opt=twistSegments, color=lcd.DARKCYAN)
            lcd.ellipse(CX, CY, radiusX, radiusNodY, 
                        opt=nodSegments, color=lcd.DARKCYAN)
        else:
            lcd.circle(noseX, noseY, 5, lcd.BLACK, lcd.BLACK)
            lcd.ellipse(CX, CY, radiusX, radiusY, color=lcd.BLACK)
            lcd.ellipse(CX, CY, radiusTwistX, radiusY,
                        opt=twistSegments, color=lcd.BLACK)
            lcd.ellipse(CX, CY, radiusX, radiusNodY, 
                        opt=nodSegments, color=lcd.BLACK)
    def draw(self):
        self._draw(True)
    
    def blank(self):
        self._draw(False)
class GUI:
    # encapsulates the menu, display, and button controls
    blubot = Head()
    B_alreadyPressed = False # used to stop auto-repeat of button
    menuQuit = False # used to exit the menu loop
    # initialise display
    WIDTH = 320
    HEIGHT = 240
    tft = lcd
    tft.init(tft.M5STACK, width=WIDTH, height=HEIGHT, rst_pin=33, backl_pin=32, 
            miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True, backl_on=1)
    def displayMenu(self):
        # FONT_Default, FONT_DefaultSmall, FONT_DejaVu18, FONT_DejaVu24
        # FONT_Ubuntu, FONT_Comic, FONT_Minya, FONT_Tooney, FONT_Small
        # FONT_7seg
        tft = self.tft
        blubot = self.blubot
        tft.font(lcd.FONT_DejaVu24, fixedwidth=False)
        tft.text(0, 0, "BluBonce", lcd.DARKCYAN)
        tft.font(lcd.FONT_Default, fixedwidth=False)
        tft.text(0, 180, "Twist:", blubot.getColour('twist'))
        tft.text(0, 195, "Nod:",  blubot.getColour('nod'))
        tft.text(0, 210, "Tilt:", blubot.getColour('tilt'))
        tft.text(0, 225, "Jaw:", blubot.getColour('jaw'))
        tft.font(lcd.FONT_Default, fixedwidth=True)
        tft.text(40, 180, str("{:3}".format(blubot.twistCurrentAngle)), 
            blubot.getColour('twist'))
        tft.text(40, 195, str("{:3}".format(blubot.nodCurrentAngle)),
            blubot.getColour('nod'))
        tft.text(40, 210, str("{:3}".format(blubot.tiltCurrentAngle)),
            blubot.getColour('tilt'))
        tft.text(40, 225, str("{:3}".format(blubot.jawCurrentAngle)),
            blubot.getColour('jaw'))
    def end(self):
        # show "game over" screen to indicate the program has terminated
        self.tft.clear()
        self.tft.font(lcd.FONT_DejaVu24, fixedwidth=False)
        self.tft.text(lcd.CENTER, lcd.CENTER, "Shutting down...", lcd.RED)
        time.sleep_ms(1000)
        self.tft.clear()
    def runMenu(self):
        blubot = self.blubot
        while self.menuQuit == False:
            self.displayMenu()
            blubot.draw()
            # can't use callback functions for B, since we already have one
            # to detect the long-press, so we check this press manually
            if btnB.isPressed():                    
                if not B_alreadyPressed:
                    # step through the different movement types - tilt, twist etc
                    blubot.setNextAxis()
                    B_alreadyPressed = True # stops it repeating until we release
            else:
                B_alreadyPressed = False
            time.sleep_ms(1)
    def buttonA_wasPressed(self):
        self.blubot.blank()
        self.blubot.moveActiveAxis(-10)
        
    def buttonB_pressFor(self):
        self.menuQuit = True
    def buttonC_wasPressed(self):
        self.blubot.blank()
        self.blubot.moveActiveAxis(10)
    def __init__(self):
        # setup callback functions for the buttons
        btnA.wasPressed(self.buttonA_wasPressed)
        btnB.pressFor(1, self.buttonB_pressFor)
        btnC.wasPressed(self.buttonC_wasPressed)


m5GUI = GUI()
m5GUI.runMenu()
m5GUI.end() # clear display to "end" screen
