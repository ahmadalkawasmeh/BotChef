#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
from time import time, sleep
from typing import Union

import RPi.GPIO as GPIO
import pyrebase

from . import messageService

"""
This script provides functions to interact with Firebase and control sauce 
dispensing.

"""

# GPIO mode setting
GPIO.setmode(GPIO.BCM)

# Firebase connection
# noinspection SpellCheckingInspection
config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com",
}

# Connecting to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_ordered_sauce(orderNum: str = "Order1") -> str:
    """
    Check the order info in Firebase and retrieve the customer's choice for
    sauce.

    Parameters:
        orderNum (str): The order number.

    Returns:
        str: The customer's sauce choice.
    """
    sauce_choice = (
        db.child("Customer")
        .child(orderNum)
        .child("OrderInfo")
        .child("Ingredients")
        .child("sauce")
        .get()
    ).val()
    return sauce_choice


def dispense_sauce(sauceVal: str) -> Union[None, bool]:
    """
    Dispense sauce by activating the sauce pump.

    Parameters:
        sauceVal (str): The sauce value indicating whether sauce
        should be dispensed.

    Returns:
        None: If the sandwich hasn't arrived.
        bool: True if sauce has been dispensed, False otherwise.
    """
    sleep(5)
    if sandwich_arrived():
        if sauceVal == "True":
            sauce_dispenser()
            print("Sauce has been dispensed")
            return True
        elif sauceVal == "False":
            print("Customer order excluded sauce, no sauce will be dispensed")
            return False
    else:
        return None


def sauce_dispenser(n: int = 2) -> bool:
    """
    Activate the sauce pump motor for a specified duration.

    Parameters:
        n (int): Duration to activate the pump in seconds. Default is 2.

    Returns:
        bool: True if the pump is activated successfully.
    """
    # Initialize Sauce Pump Relay
    GPIO.setmode(GPIO.BCM)
    PUMP = 21
    GPIO.setup(PUMP, GPIO.OUT)

    GPIO.output(PUMP, True)
    sleep(n)
    GPIO.output(PUMP, False)
    GPIO.cleanup()

    return True


def sandwich_arrived() -> bool:
    """
    Implement the IR proximity sensor to detect sandwich arrival.

    Returns:
        bool: True if the sandwich has arrived, False otherwise.
    """
    # Initializing IR Proximity Sensor
    GPIO.setmode(GPIO.BCM)
    PROX = 17
    GPIO.setup(PROX, GPIO.IN)

    if GPIO.input(PROX) == GPIO.LOW:
        GPIO.cleanup()
        return True
    else:
        return False


def get_db_sauce_level() -> int:
    """
    Retrieve sauce level stored in Firebase.

    Returns:
        int: The sauce level retrieved from Firebase.
    """
    sauce_level = (
        db.child("Employee").child("IngredientsLevel").child("sauce").get()
    ).val()
    return sauce_level


def get_sauce_sensor_reading() -> float:
    """
    Check the sauce level in the sauce reservoir using an ultrasonic sensor.

    Returns:
        float: The distance reading from the ultrasonic sensor.
    """
    # Initializing Ultrasonic Sensor
    GPIO.setmode(GPIO.BCM)
    # Define sensor GPIO pins
    TRIG = 12
    ECHO = 27
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


def get_sauce_reservoir_level() -> float:
    """
    Calculate the sauce level in the reservoir based on sensor readings.

    Returns:
        float: The calculated reservoir level.
    """
    sensor_reading = get_sauce_sensor_reading()
    RESERVOIR_HEIGHT = 17
    reservoir_level = round(RESERVOIR_HEIGHT - sensor_reading, 1)
    return reservoir_level


def update_sauce_level():
    """
    Update sauce level in Firebase with the current reservoir level.
    """
    new_sauce_level = get_sauce_reservoir_level()
    # Overwrite sauce level in Firebase with updated level
    db.child("Employee").child("IngredientsLevel").child("sauce").set(
        new_sauce_level
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


def notify_employee(employeeNum: str = "Employee1"):
    """
    Notify employee when sauce level is low.

    Parameters:
        employeeNum (str): The identifier of the employee. Default is
        "Employee1".
    """
    current_level = get_db_sauce_level()
    employee_phone = get_employee_phone(employeeNum)
    msg_body = messageService.parse_message(0, current_level)
    messageService.send_sms_message(msg_body, employee_phone)
    print(
        "Low sauce notification sent to : "
        + str(employeeNum)
        + " , and the phone number is "
        + str(employee_phone)
    )
    sauce_refill()


def sauce_refill():
    """
    Update Firebase after refilling the sauce reservoir.

    """
    update_sauce_level()
    print(
        "Sauce level has been replenished to : "
        + str(get_sauce_reservoir_level())
    )
