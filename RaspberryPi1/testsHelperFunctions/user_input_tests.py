import pyrebase
import time
import app
from RPLCD import CharLCD
from display import initialize_lcd, display_message, get_message
"""test module for user input"""

config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def insert_employee_data_test(data):
    """Test inserting employee data into the database and validate the inserted data."""
    if data['type'] == 'employee':
        name_e = db.child('Employee').child('Employees').child('Employee1').child('name').set(data.get('name'))
        email_e = db.child('Employee').child('Employees').child('Employee1').child('email').set(data.get('email'))
        phone_e = db.child('Employee').child('Employees').child('Employee1').child('phone').set(data.get('phoneNumber'))

        name_e_actual = db.child('Employee').child('Employees').child('Employee1').child('name').get().val()
        email_e_actual = db.child('Employee').child('Employees').child('Employee1').child('email').get().val()
        phone_e_actual = db.child('Employee').child('Employees').child('Employee1').child('phone').get().val()

        try:
            assert name_e == name_e_actual
            print("Test passed: name")
        except AssertionError:
            print("Test failed")

        try:
            assert email_e == email_e_actual
            print("Test passed: email")
        except AssertionError:
            print("Test failed")

        try:
            assert phone_e == phone_e_actual
            print("Test passed: phone")
        except AssertionError:
            print("Test failed")


def insert_customer_data_test(data):
    """Test inserting customer data into the database and validate the inserted data."""
    if data['type'] == 'customer':
        name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('name'))
        phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('phoneNumber'))
        email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('email'))
       
        name_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
        email_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
        phone_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()

        try:
            assert name_c == name_c_actual
            print("Test passed: name")
        except AssertionError:
            print("Test failed")

        try:
            assert email_c == email_c_actual
            print("Test passed: email")
        except AssertionError:
            print("Test failed")

        try:
            assert phone_c == phone_c_actual
            print("Test passed: phone")
        except AssertionError:
            print("Test failed")


def lcd_on_test():
    """Test turning on the LCD screen and validate the message displayed."""
    lcd = initialize_lcd()
    display_message(lcd, "On")

    try:
        assert get_message(lcd) == "On"
        print("Test passed: lcd_on")
    except AssertionError:
        print("Test failed")


def order_progress_test():
    """Test the progress of the order and validate the messages displayed on the LCD screen."""
    lcd = initialize_lcd()
    display_message(lcd, "start")
    assert get_message(lcd) == "start"
    time.sleep(10)
    display_message(lcd, "end")
    assert get_message(lcd) == "end"


def customer_name_test(user_name_c):
    """Test the customer name stored in the database and validate it."""
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
   
    try:
        assert orig_name_c == user_name_c
        print("Test passed: customer name")
    except AssertionError:
        print("Test failed")


def customer_email_test(user_email_c):
    """Test the customer email stored in the database and validate it."""
    orig_email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
   
    try:
        assert user_email_c == orig_email_c
        print("Test passed: customer email")
    except AssertionError:
        print("Test failed")


def customer_phone_test(user_phone_c):
    """Test the customer phone number stored in the database and validate it."""
    orig_phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()
   
    try:
        assert user_phone_c == orig_phone_c
        print("Test passed: customer phone")
    except AssertionError:
        print("Test failed")


def employee_name_test():
    """Test the employee name stored in the database and validate it."""
    orig_name_e = db.child('Employee').child('Order1').child('CustomerInfo').child('name').get().val()
    try:
        assert user_name_e == orig_name_e
        print("Test passed: employee name")
    except AssertionError:
        print("Test failed")
       

def employee_email_test():
    """Test the employee email stored in the database and validate it."""
    orig_email_e = db.child('Employee').child('Order1').child('CustomerInfo').child('email').get().val()
    try:
        assert user_email_e == orig_email_e
        print("Test passed: employee email")
    except AssertionError:
        print("Test failed")


def employee_phone_test():
    """Test the employee phone number stored in the database and validate it."""
    orig_phone_e = db.child('Employee').child('Order1').child('CustomerInfo').child('phone').get().val()
    try:
        assert user_phone_e == orig_phone_e
        print("Test passed: employee phone")
    except AssertionError:
        print("Test failed")
   

def validate_user_inputs(data):
    """Validate user inputs."""
    if 'customerEmail' in data:
        cust_email = data.get('customerEmail')
        validate_customer_email(cust_email)
    if 'customerPhoneNumber' in data:
        cust_phone = data.get('customerPhoneNumber')
        validate_customer_phone(cust_phone)
    if 'employeeEmail' in data:
        emp_email = data.get('employeeEmail')
        validate_employee_email(emp_email)
    if 'employeePhoneNumber' in data:
        emp_phone = data.get('employeePhoneNumber')
        validate_employee_phone(emp_phone)


def validate_customer_email(email):
    """Validate the customer email format."""
    assert '@' in email


def validate_customer_phone(phone):
    """Validate the customer phone number format."""
    assert phone.startswith('+1') and len(phone) == 12


def validate_employee_email(email):
    """Validate the employee email format."""
    assert '@' in email


def validate_employee_phone(phone):
    """Validate the employee phone number format."""
    assert phone.startswith('+1') and len(phone) == 12
