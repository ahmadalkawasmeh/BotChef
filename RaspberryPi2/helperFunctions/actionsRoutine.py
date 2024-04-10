# Author: Zach
# Some functions based off code written by Ahmed
# This program contains functions related to the operation of Pi2 (bread pi) within the system
# Responsible for hardware/sensors and firebase updates

from time import time, sleep
import RPi.GPIO as GPIO
import RpiMotorLib import RpiMotorLib, rpiservolib
import pyrebase
from . import messagingRoutine

# GPIO mode setting
GPIO.setmode(GPIO.BCM)

# Firebase connection
config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com",
}

# Connecting to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def update_bread_level():
    """
    Update bread level in Firebase with the current sensor reading
    """
    new_bread_level = get_bread_hopper_level()
    # Overwrite sauce level in Firebase with updated level
    db.child("Employee").child("IngredientsLevel").child("bread").set(
        new_bread_level
    )

def get_bread_hopper_level() -> float:
    """
    Calculate the bread level in the hopper based on sensor readings.

    Returns:
        float: The calculated hopper level.
    """
    sensor_reading = get_bread_sensor_reading()
    BREAD_HEIGHT = 1.6 #Height of 1 bread slice
    HEIGHT_OFFSET = 0
    bread_level = round((sensor_reading-HEIGHT_OFFSET)/BREAD_HEIGHT, 1)
    return bread_level

def get_bread_sensor_reading() -> float:
    """
    Check the bread level in the hopper using an ultrasonic sensor.

    Returns:
        float: The distance reading from the ultrasonic sensor.
    """
    # Initializing Ultrasonic Sensor
    GPIO.setmode(GPIO.BCM)
    # Define sensor GPIO pins
    TRIG = 4
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time()
    pulse_end = time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s

    distance = round(distance, 1)
    GPIO.cleanup()
    return distance

def get_db_bread_level() -> int:
    """
    Retrieve bread level stored in Firebase.

    Returns:
        int: The bread level retrieved from Firebase.
    """
    bread_level = (
        db.child("Employee").child("IngredientsLevel").child("bread").get()
    ).val()
    return bread_level

def notify_employee(employeeNum: str = "Employee1"):
    """
    Notify employee when bread level is low.

    Parameters:
        employeeNum (str): The identifier of the employee. Default is
        "Employee1".
    """
    current_level = get_db_bread_level()
    employee_phone = get_employee_phone(employeeNum)
    msg_body = messagingRoutine.parse_message(0, current_level)
    messagingRoutine.send_sms_message(msg_body, employee_phone)
    print(
        "Low bread notification sent to : "
        + str(employeeNum)
        + " , and the phone number is "
        + str(employee_phone)
    )

def get_employee_phone(employeeNum: str = "Employee1") -> str:
    """
    Retrieve the employee's phone number from Firebase.

    Parameters:
        employeeNum (str): The identifier of the employee. Default is
        "Employee1".

    Returns:
        str: The phone number of the specified employee.
    """
    return (
        db.child("Employee")
        .child("Employees")
        .child(employeeNum)
        .child("phone")
        .get()
    ).val()

def dispense_bread() -> None:
    #dispense it
    SERVO = 5
    myServo = rpiservolib.SG90servo("servoOne", 50, 2, 12)
    myServo.servo_move(SERVO, 10, 1, False, 0.01)
    sleep(2)
    myServo.servo_move(SERVO, 3, 1, False, 0.01)
    sleep(3)

def move_belt(steps, dir) -> None:
    """
    Move stepper a certain number of steps
    direction:
    True -> right
    False -> left
    """
    #Move
    DIRECTION = 6
    STEP = 26
    myMotor = RpiMotorLib.A4988Nema(DIRECTION, STEP, (-1,-1,-1))
    myMotor.motor_go(dir, "Full", steps, 0.01, False, 0.05)
    sleep(1)
