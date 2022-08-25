# As of 12/4/20
# BluBot Head Servo control software
# by Luis Villazon
# released into the public domain
# https://m5stack.com/products/servo-module
# https://github.com/m5stack/M5Stack_MicroPython

# REFERENCE WEBSITES
# https://github.com/m5stack/UIFlow-Code/wiki/Display
# https://docs.python.org/3/tutorial/classes.html
# https://www.tutorialspoint.com/python/python_lists.htm
# <-- max line length to comply with PEP-8 (79 chars) ------------------------->
from m5stack import *
from machine import Pin, PWM
import i2c_bus
import math
import time

SERVO_ENABLE = True

# set to false to disable servos for testing
POSE_FREESTYLE_ENABLE = False # when False you can only use pre-defined poses

SELECTED_COLOUR = lcd.CYAN
MENU_COLOUR = lcd.DARKCYAN

# initialise i2c bus
i2c = i2c_bus.easyI2C((21, 22), 0x53)
if SERVO_ENABLE:
    debugMessage = ""
else:
    debugMessage = "No Servo"

class Head:
    def __init__(self):
        self.servoRestAngles = {'throat': 90,
                            'crown':  90,
                            'left neck': 90,
                            'right neck': 90,
                            }
        self.servoAngles = {'throat': self.servoRestAngles['throat'],
                            'crown':  self.servoRestAngles['crown'],
                            'left neck': self.servoRestAngles['left neck'],
                            'right neck': self.servoRestAngles['right neck'],
                            }
        self.servoChannels = {'throat': 0,
                             'crown':  1,
                             'left neck': 2,
                             'right neck': 3,
                             }
        self.servoNames = ['throat',
                           'crown',
                           'right neck',
                           'left neck',
                           ]
        self.activeServo = self.servoNames[0]
        self.poseNames = ['default',
                          'ahead',
                          'down',
                          'up',
                          'left',
                          'right',
                          'up & left',
                          'up & right',
                          'down & left',
                          'down & right',
                          ]
        self.currentPose = 'default'
        # override the SERVO_ENABLE flag temporarily to set the rest position
        global SERVO_ENABLE
        saveServoState = SERVO_ENABLE
        SERVO_ENABLE = True
        self.restPose()
        SERVO_ENABLE = saveServoState
        
        self._eyePWM = PWM(Pin(26), freq=1000, duty=0)
    
    def eyesOn(self, fadeUpTime=1000):
        for i in range(0, 100):
            self._eyePWM.duty(i)
            time.sleep_ms(int(fadeUpTime/100))

    def eyesFade(self, fadeDownTime=1000):
        for i in range(100, 5, -1):
            self._eyePWM.duty(i)
            time.sleep_ms(int(fadeDownTime/100))

    def eyesOff(self):
        self._eyePWM.duty(0)
        
    def setNextServo(self):
        self.activeServo = self.servoNames[
            (self.servoNames.index(self.activeServo) + 1) 
            % len(self.servoNames)]

    def setServo(self, channel, angle):
        # the 0x10 tells the write function to use pwm to drive the servo to the
        # specified angle
        if SERVO_ENABLE == True:
            i2c.write_u8(channel + 0x10, angle)

    def moveActiveServo(self, angleChange):
        # increment/decrement the currently active servo
        self.servoAngles[self.activeServo] += angleChange
        if self.servoAngles[self.activeServo] < 0:
            self.servoAngles[self.activeServo] = 0
        if self.servoAngles[self.activeServo] > 180:
            self.servoAngles[self.activeServo] = 180
        global debugMessage
        debugMessage = ("ch" + str(self.servoChannels[self.activeServo]) +
                        " pos=" + str(self.servoAngles[self.activeServo]))
        self.setServo(self.servoChannels[self.activeServo],
                      round(self.servoAngles[self.activeServo]))

    def restPose(self):
        for i in self.servoNames:
            self.servoAngles[i] = self.servoRestAngles[i]
            self.setServo(self.servoChannels[i], self.servoAngles[i])

    def setPose(self, pose):
        global debugMessage
        debugMessage = pose
        if pose == 'default':
            # ahead pose (non normalised)
            newThroatAngle = 90
            newCrownAngle = 115
            newRNeckAngle = 90
            newLNeckAngle = 90
        if pose == 'ahead':
            newThroatAngle = self.servoRestAngles['throat']
            newCrownAngle = self.servoRestAngles['crown']
            newRNeckAngle = self.servoRestAngles['right neck']
            newLNeckAngle = self.servoRestAngles['left neck']
        if pose == 'up':
            # empirically determined target angles
            newThroatAngle = 150
            newCrownAngle = 90
            newRNeckAngle = 90
            newLNeckAngle = 90
        if pose == 'down':
            # empirically determined target angles
            newThroatAngle = 80
            newCrownAngle = 90
            newRNeckAngle = 90
            newLNeckAngle = 90
        if pose == 'right':
            # empirically determined target angles
            newThroatAngle = 127
            newCrownAngle = 44
            newRNeckAngle = 90
            newLNeckAngle = 90
        if pose == 'left':
            # empirically determined target angles
            newThroatAngle = 127
            newCrownAngle = 140
            newRNeckAngle = 90
            newLNeckAngle = 90
        if pose == 'up & left':
            # empirically determined target angles
            newThroatAngle = 155
            newCrownAngle = 140
            newRNeckAngle = 135
            newLNeckAngle = 45
        if pose == 'up & right':
            # empirically determined target angles
            newThroatAngle = 155
            newCrownAngle = 40
            newRNeckAngle = 45
            newLNeckAngle = 135
        if pose == 'down & right':
            # empirically determined target angles
            newThroatAngle = 80
            newCrownAngle = 40
            newRNeckAngle = 135
            newLNeckAngle = 45
        if pose == 'down & left':
            # empirically determined target angles
            newThroatAngle = 80
            newCrownAngle = 140
            newRNeckAngle = 45
            newLNeckAngle = 135

        # interpolate to these positions
        steps = 1
        if steps > 1:
            throatStep = (
                            (newThroatAngle - self.servoAngles['throat'])
                            /steps)
            crownStep = (
                        (newCrownAngle - self.servoAngles['crown'])
                        /steps)
            leftNeckStep = (
                            (newLNeckAngle - self.servoAngles['left neck'])
                            /steps)
            rightNeckStep = (
                            (newRNeckAngle - self.servoAngles['right neck'])
                            /steps)
            for i in range(steps):
                self.activeServo = 'throat'
                self.moveActiveServo(throatStep)
                self.activeServo = 'crown'
                self.moveActiveServo(crownStep)
                self.activeServo = 'left neck'
                self.moveActiveServo(leftNeckStep)
                self.activeServo = 'right neck'
                self.moveActiveServo(rightNeckStep)
                time.sleep_ms(1)

        # explicitly set servo angles to the target values
        # to account for possible rounding errors during interpolation
        self.setServo(self.servoChannels['throat'], newThroatAngle)
        self.setServo(self.servoChannels['crown'], newCrownAngle)
        self.setServo(self.servoChannels['left neck'], newLNeckAngle)
        self.setServo(self.servoChannels['right neck'], newRNeckAngle)

        # record new servo positions
        self.servoAngles['throat'] = newThroatAngle
        self.servoAngles['crown'] = newCrownAngle
        self.servoAngles['left neck'] = newLNeckAngle
        self.servoAngles['right neck'] = newRNeckAngle
        self.currentPose = pose

        if pose == 'ahead': # Terminator eyes!
            # wait for the servos to get there
            time.sleep_ms(1000)
            # briefly fade up the eyes
            self.eyesOn(3000)
            time.sleep_ms(1000)
            self.eyesFade()
            self.eyesOff()

    
    def getNextPose(self, pose):
        # selects the next pose from the list of predefined ones
        name = self.poseNames[
                              (self.poseNames.index(pose) + 1)
                              % len(self.poseNames)
                             ]
        return name

    def getPrevPose(self, pose):
        # selects the next pose from the list of predefined ones
        name = self.poseNames[
                              (self.poseNames.index(pose) - 1)
                              % len(self.poseNames)
                             ]
        return name

class GUI:
    # encapsulates the menu, display, and button controls
    butAlreadyPressed = False # used to stop auto-repeat of button
    menuQuit = False # used to exit the menu loop
    # initialise display
    WIDTH = 320
    HEIGHT = 240
    tft = lcd
    tft.init(tft.M5STACK, width=WIDTH, height=HEIGHT, rst_pin=33, backl_pin=32, 
            miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True, backl_on=1)
    
    def servoMenu(self):
        # FONT_Default, FONT_DefaultSmall, FONT_DejaVu18, FONT_DejaVu24
        # FONT_Ubuntu, FONT_Comic, FONT_Minya, FONT_Tooney, FONT_Small
        # FONT_7seg
        global debugMessage
        tft = self.tft
        tft.font(lcd.FONT_DejaVu24, fixedwidth=False)
        tft.text(0, 0, "BluBonce", MENU_COLOUR)
        tft.text(140,0, debugMessage, lcd.RED)

        # display current servo angles
        tft.font(lcd.FONT_DejaVu18, fixedwidth=False)
        rowPosition = 40
        rowHeight = 20
        for i in blubot.servoNames:
            if i == blubot.activeServo:
                colour = SELECTED_COLOUR
            else:
                colour = MENU_COLOUR
            tft.text(0, rowPosition, i, colour)
            tft.text(110, rowPosition, 
                     str("{:3}".format(blubot.servoAngles[i])), colour)
            rowPosition += rowHeight

        # can't use callback functions for B, since we already have one
        # to detect the long-press, so we check this press manually
        if btnB.isPressed():                    
            if not self.B_alreadyPressed:
                # step through the different movement types - tilt, twist etc
                blubot.setNextServo()
                self.B_alreadyPressed = True # stops it repeating until we release
        else:
            self.B_alreadyPressed = False


    def poseMenu(self):
        # FONT_Default, FONT_DefaultSmall, FONT_DejaVu18, FONT_DejaVu24
        # FONT_Ubuntu, FONT_Comic, FONT_Minya, FONT_Tooney, FONT_Small
        # FONT_7seg
        global debugMessage
        tft = self.tft
        tft.font(lcd.FONT_DejaVu24, fixedwidth=False)
        tft.text(0, 0, "BluBonce", MENU_COLOUR)
        tft.text(140,0, debugMessage, lcd.RED)

        # display available poses
        tft.font(lcd.FONT_DejaVu18, fixedwidth=False)
        rowPosition = 40
        rowHeight = 20
        for i in blubot.poseNames:
            # mark the cursor position
            if i == self.selectedPose:
                colour = lcd.RED
            else:
                colour = lcd.BLACK
            tft.text(0, rowPosition, '->', colour) # cursor position

            if i == blubot.currentPose:
                colour = SELECTED_COLOUR # highlight current pose
            else:
                colour = MENU_COLOUR
            tft.text(40, rowPosition, i, colour)

            rowPosition += rowHeight

        # can't use callback functions for B, since we already have one
        # to detect the long-press, so we check this press manually
        if btnB.isPressed():
            if not self.B_alreadyPressed:
                # step through the different movement types - tilt, twist etc
                blubot.setPose(self.selectedPose)
                self.B_alreadyPressed = True # stops it repeating until we release
        else:
            self.B_alreadyPressed = False
 
    def chooseMenu(self):
        while self.menuQuit == False:
            if POSE_FREESTYLE_ENABLE:
                self.servoMenu()
            else:
                self.poseMenu()
        time.sleep_ms(1)

    def end(self):
        # show "game over" screen to indicate the program has terminated
        self.tft.clear()
        self.tft.font(lcd.FONT_DejaVu24, fixedwidth=False)
        self.tft.text(lcd.CENTER, lcd.CENTER, "Shutting down...", lcd.RED)
        blubot.restPose()
        time.sleep_ms(1000)
        self.tft.clear()
    
    def buttonA_wasPressed(self):
        if POSE_FREESTYLE_ENABLE:
            blubot.moveActiveServo(-1)
        else:
            # cycle through the available poses
            self.selectedPose = blubot.getPrevPose(self.selectedPose)
        
    def buttonB_pressFor(self):
        self.menuQuit = True
    
    def buttonC_wasPressed(self):
        if POSE_FREESTYLE_ENABLE:
            blubot.moveActiveServo(1)
        else:
            # cycle through the available poses
            self.selectedPose = blubot.getNextPose(self.selectedPose)
    
    def __init__(self):
        # setup callback functions for the buttons
        btnA.wasPressed(self.buttonA_wasPressed)
        btnB.pressFor(1, self.buttonB_pressFor)
        btnC.wasPressed(self.buttonC_wasPressed)
        self.selectedPose = 'ahead'


def demo(blubot):
    while not btnB.isPressed():
        time.sleep_ms(50)
    time.sleep_ms(3000)
    blubot.setPose('up & left')
    time.sleep_ms(2000)
    blubot.setPose('right')
    time.sleep_ms(2000)
    blubot.setPose('up')
    time.sleep_ms(2000)
    blubot.setPose('ahead')

blubot = Head()
#demo(blubot)
m5GUI = GUI()
m5GUI.chooseMenu()
m5GUI.end() # clear display to "end" screen
