# Author: Zach Gregory
# This is the program for the unit test demo of Pi2 (bread/conveyor pi) and its associated hardware. 
# Run this program and use keyboard inputs to proceed through the test procedures
# Observe the hardware and ensure that it performs the expected actions

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from gpiozero import Servo
from Bluetin_Echo import Echo
import time


GPIO.setmode(GPIO.BCM)

DIRECTION = 6
STEP = 26
motorTest = RpiMotorLib.A4988Nema(DIRECTION, STEP, (21,21,21), "A4988")

TRIG = 18
ECHO = 24
myEcho = Echo(TRIG,ECHO, 343)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

servo = Servo(5)

testing = True

#Test procedure: 

#Test 1 - 2 stepper rotations in each direction
#Press enter to begin the next test
#Test 2 - Rotate servo 120 degrees in each direction twice
#Press enter to begin the next test
#Test 3 - Ultrasonic sensor @ 20cm
#Tests complete

while testing:
    #Test 1 - Stepper Motor
    print()
    print("Test 1 - expected outcome: 2 full rotations in each direction")
    input("Press enter to begin the first test (Stepper Test)")
    motorTest.motor_go(False, "Full" , 400, .01, False, .05)
    time.sleep(1)
    motorTest.motor_go(True, "Full" , 400, .01, False, .05)
    time.sleep(1)

    #Test 2 - Servo
    print("Test 2 - expected outcome: 120 degrees in each direction twice")
    input("Press enter to continue to the next test (Servo Test)")
    servo.min() #0 deg
    time.sleep(2)
    servo.max() #120 deg
    time.sleep(2)
    servo.min() #0 deg
    time.sleep(2)
    servo.max() #120 deg
    time.sleep(2)
    servo.min() #0 deg

    #Test 3 - Ultrasonic
    print("Test 3 - expected outcome: 20cm reading")
    print("Place an object 20cm in front of the sensor")
    input("Press enter to continue to the next test (Ultrasonic Test)")

    dist = myEcho.read('cm',10)
    print("Distance: ", dist)
    if dist < 0.21 and dist > 0.19:
        print("Test passed")
    else:
        print("Test failed")

    print("Tests complete")
    inp = input("Press y to run tests again, or any other key to exit")
    if inp != "y":
        testing = False

GPIO.cleanup()
