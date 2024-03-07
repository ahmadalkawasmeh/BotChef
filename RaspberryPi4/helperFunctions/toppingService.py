import pyrebase

from RaspberryPi4.helperFunctions import messageService

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


# Check the order info in Firebase and retrieve the customer's choice for topping
def get_ordered_topping(orderNum="Order1"):
    topping_choice = (
        db.child("Customer").child(orderNum).child("OrderInfo").child("Ingredients").child("topping").get()).val()
    return topping_choice


# Dispense topping by activating servo motor
def dispense_topping(toppingVal):
    if toppingVal == "True":
        print("Topping has been dispensed")
    if toppingVal == "False":
        print("Customer order excluded toppings, no toppings will be dispensed")


# Retrieve topping level stored in Firebase
def check_topping_level():
    topping_level = (db.child("Employee").child("IngredientsLevel").child("topping").get()).val()
    return topping_level


# Decrement topping level in Firebase
def update_topping_level(n=1):
    # Retrieve current topping level and decrement
    current_topping_level = (db.child("Employee").child("IngredientsLevel").child("topping").get()).val()
    new_topping_level = current_topping_level - n
    # Overwrite topping level in Firebase with updated level
    db.child("Employee").child("IngredientsLevel").child("topping").set(new_topping_level)


# Retrieve the employee's phone number from the Firebase
def get_employee_phone(employeeNum="Employee1"):
    return (db.child("Employee").child("Employees").child(employeeNum).child("phone")).val()


# Notify employee when topping level is low
def notify_employee(employeeNum="Employee1"):
    current_level = check_topping_level()
    employee_phone = get_employee_phone(employeeNum)
    msg_body = messageService.parse_message(0, current_level)
    messageService.send_sms_message(msg_body, employee_phone)
    print("Low topping notification sent to : " + str(employeeNum) + " , and the phone number is " + str(employee_phone))
    topping_refill()


def topping_refill(fullLevel=10):
    db.child("Employee").child("IngredientsLevel").child("topping").set(fullLevel)
    print("topping level has been replenished to : " + str(fullLevel))
