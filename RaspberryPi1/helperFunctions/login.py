import pyrebase

from . import messageService

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
def get_customer_name(orderNum="Order1"):
    customer_name = (
        db.child("Customer").child(orderNum).child("CustomerInfo").child("name").get()).val()
    return customer_name


# Dispense topping by activating servo motor
def get_customer_email(orderNum="Order1"):
    customer_email = (
        db.child("Customer").child(orderNum).child("CustomerInfo").child("email").get()).val()
    return customer_email

# Retrieve topping level stored in Firebase
def get_customer_phone(orderNum="Order1"):
    customer_phone = (
        db.child("Customer").child(orderNum).child("CustomerInfo").child("phone").get()).val()
    return customer_phone

# Decrement topping level in Firebase
def get_employee_name():
    employee_name = (
        db.child("Employee").child("Employees").child("Employee1").child("name").get()).val()
    return employee_name


# Dispense topping by activating servo motor
def get_employee_email():
    employee_email = (
        db.child("Employee").child("Employees").child("Employee1").child("email").get()).val()
    return employee_email

# Retrieve topping level stored in Firebase
def get_employee_phone():
    employee_phone = (
        db.child("Employee").child("Employees").child("Employee1").child("phone").get()).val()
    return employee_phone




