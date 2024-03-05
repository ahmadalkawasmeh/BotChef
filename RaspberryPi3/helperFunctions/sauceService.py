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
def get_ordered_sauce(orderNum = "order1"):
    sauce_choice = (
        db.child("Customer").child(orderNum).child("orderInfo").child("ingredients").child("sauce").get()).val()
    return sauce_choice


# Dispense sauce by activating sauce pump
def dispense_sauce(sauceVal):
    if sauceVal == "True":
        print("Sauce has been dispensed")
        return True
    if sauceVal == "False":
        print("Customer order excluded sauce, no sauce will be dispensed")
        return False


# Retrieve sauce level stored in Firebase
def check_sauce_level():
    sauce_level = (db.child("Employee").child("IngredientLevel").child("sauce").get()).val()
    return sauce_level


# Decrement sauce level in Firebase
def update_sauce_level():
    # Retrieve current sauce level and decrement
    current_sauce_level = (db.child("Employee").child("IngredientLevel").child("sauce").get()).val()
    new_sauce_level = current_sauce_level - 1
    # Overwrite sauce level in Firebase with updated level
    db.child("Employee").child("IngredientLevel").child("sauce").set(new_sauce_level)


# Retrieve the employee's phone number from the Firebase
def get_employee_phone(employeeNum):
    return (db.child("Employee").child("Employees").child("Employee" + str(employeeNum)).child("phone")).val()


# Notify employee when sauce level is low
def notify_employee(employeeNum = "Employee1"):
    current_level = check_sauce_level()
    employee_phone = get_employee_phone(employeeNum)
    message = messageService.parse_message(0, current_level)
    messageService.send_message(message, employee_phone)
    print("Low sauce notification sent to : " + str(employeeNum) + " , and the phone number is " + str(employee_phone))
