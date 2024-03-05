import pyrebase

from RaspberryPi3.helperFunctions import messageService

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
    if sauceVal == "True":
        print("Sauce has been dispensed")
    if sauceVal == "False":
        print("Customer order excluded sauce, no sauce will be dispensed")


# Retrieve sauce level stored in Firebase
def check_sauce_level():
    sauce_level = (db.child("Employee").child("IngredientsLevel").child("sauce").get()).val()
    return sauce_level


# Decrement sauce level in Firebase
def update_sauce_level(n=1):
    # Retrieve current sauce level and decrement
    current_sauce_level = (db.child("Employee").child("IngredientsLevel").child("sauce").get()).val()
    new_sauce_level = current_sauce_level - n
    # Overwrite sauce level in Firebase with updated level
    db.child("Employee").child("IngredientsLevel").child("sauce").set(new_sauce_level)


# Retrieve the employee's phone number from the Firebase
def get_employee_phone(employeeNum="Employee1"):
    return (db.child("Employee").child("Employees").child(employeeNum).child("phone")).val()


# Notify employee when sauce level is low
def notify_employee(employeeNum="Employee1"):
    current_level = check_sauce_level()
    employee_phone = get_employee_phone(employeeNum)
    msg_body = messageService.parse_message(0, current_level)
    messageService.send_sms_message(msg_body, employee_phone)
    print("Low sauce notification sent to : " + str(employeeNum) + " , and the phone number is " + str(employee_phone))
    sauce_refill()


def sauce_refill(fullLevel=10):
    db.child("Employee").child("IngredientsLevel").child("sauce").set(fullLevel)
    print("Sauce level has been replenished to : " + str(fullLevel))
