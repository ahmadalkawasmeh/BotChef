#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
import pyrebase
import RPi.GPIO as GPIO
from time import time, sleep
from . import messageService

GPIO.setmode(GPIO.BCM)
# Firebase connection parameters
config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com"
}

# Connecting to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# Check the order info in Firebase and retrieve the customer's choice for sauce
def get_ordered_sauce(orderNum="Order1"):
    sauce_choice = (
        db.child("Customer").child(orderNum).child("OrderInfo").child("Ingredients").child("sauce").get()).val()
    return sauce_choice


# Dispense sauce by activating sauce pump
def dispense_sauce(sauceVal):
    if sandwich_arrived():
        if sauceVal == "True":
            sauce_dispenser()
            print("Sauce has been dispensed")
        elif sauceVal == "False":
            print("Customer order excluded sauce, no sauce will be dispensed")

    else:
        return None


# Activate sauce pump motor for n seconds, default=2
def sauce_dispenser(n=2):
    # Initialize Sauce Pump Relay
    GPIO.setmode(GPIO.BCM)
    PUMP = 21
    GPIO.setup(PUMP, GPIO.OUT)

    GPIO.output(PUMP, True)
    sleep(2)
    GPIO.output(PUMP, False)
    GPIO.cleanup()

    return True


# Implement the IR proximity sensor
def sandwich_arrived():
    # Initializing IR Proximity Sensor
    GPIO.setmode(GPIO.BCM)
    PROX = 17
    GPIO.setup(PROX, GPIO.IN)

    if GPIO.input(PROX) == GPIO.LOW:
        GPIO.cleanup()

        return True
    else:
        return False


# Retrieve sauce level stored in Firebase
def get_db_sauce_level():
    sauce_level = (db.child("Employee").child("IngredientsLevel").child("sauce").get()).val()
    return sauce_level


# Check the sauce level in the sauce reservoir
def get_res_sauce_level():
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

    distance = round(distance, 2)
    GPIO.cleanup()
    return distance


# Decrement sauce level in Firebase
def update_sauce_level(n=1):
    # ToDo update firebase with reservoir sauce level
    # Retrieve current sauce level and decrement
    current_sauce_level = (db.child("Employee").child("IngredientsLevel").child("sauce").get()).val()
    new_sauce_level = current_sauce_level - n
    # Overwrite sauce level in Firebase with updated level
    db.child("Employee").child("IngredientsLevel").child("sauce").set(new_sauce_level)


# Retrieve the employee's phone number from the Firebase
def get_employee_phone(employeeNum="Employee1"):
    return (db.child("Employee").child("Employees").child(employeeNum).child("phone").get()).val()


# Notify employee when sauce level is low
def notify_employee(employeeNum="Employee1"):
    current_level = get_db_sauce_level()
    employee_phone = get_employee_phone(employeeNum)
    msg_body = messageService.parse_message(0, current_level)
    messageService.send_sms_message(msg_body, employee_phone)
    print("Low sauce notification sent to : " + str(employeeNum) + " , and the phone number is " + str(employee_phone))
    sauce_refill()


# Used to refill the sauce reservoir
# ToDo change when reservoir sensor is implemented
def sauce_refill(fullLevel=10):
    db.child("Employee").child("IngredientsLevel").child("sauce").set(fullLevel)
    print("Sauce level has been replenished to : " + str(fullLevel))
