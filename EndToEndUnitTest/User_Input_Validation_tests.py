   
import RPi.GPIO as GPIO
from RPLCD import CharLCD
from display import initialize_lcd, display_message, get_message
import pyrebase
import time

import app

config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print("Beginning of database tests")

def insert_employee_data_test(data):
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

print("Beginning of hardware tests")

def lcd_on_test():
    lcd = initialize_lcd()
    display_message(lcd, "On")

    try:
        assert get_message(lcd) == "On"
        print("Test passed: lcd_on")
    except AssertionError:
        print("Test failed")

print("Beginning of software tests")

lcd = initialize_lcd()
def order_progress_test():
    lcd = initialize_lcd()
    display_message(lcd, "start")
    assert get_message(lcd) == "start"
    time.sleep(10)
    display_message(lcd, "end")
    assert get_message(lcd) == "end"

def customer_name_test(user_name_c):
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
    
    try:
        assert orig_name_c==user_name_c
        print("Test passed: customer name")
    except AssertionError:
        print("Test failed")


def customer_email_test(user_email_c):
    orig_email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
    try:
        assert user_email_c == orig_email_c
        print("Test passed: customer email")
    except AssertionError:
        print("Test failed")

def customer_phone_test(user_phone_c):
    orig_phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()
    try:
        assert user_phone_c == orig_phone_c
        print("Test passed: customer phone")
    except AssertionError:
        print("Test failed")

def employee_name_test():
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()

def employee_email_test():
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()

def employee_phone_test():
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()

def validate_user_inputs(data):
    if 'customerEmail' in data:
        customer_email = data.get('customerEmail')
        assert_customer_email(customer_email)
    if 'customerPhoneNumber' in data:
        customer_phone = data.get('customerPhoneNumber')
        assert_customer_phone(customer_phone)
    if 'employeeEmail' in data:
        employee_email = data.get('employeeEmail')
        assert_employee_email(employee_email)
    if 'employeePhoneNumber' in data:
        employee_phone = data.get('employeePhoneNumber')
        assert_employee_phone(employee_phone)
        
def assert_customer_email(email):
    assert '@' in email, "Invalid customer email format"

def assert_customer_phone(phone):
    assert phone.startswith('+1') and len(phone) == 12, "Invalid customer phone number format"

def assert_employee_email(email):
    assert '@' in email, "Invalid employee email format"

def assert_employee_phone(phone):
    assert phone.startswith('+1') and len(phone) == 12, "Invalid employee phone number format"




if __name__ == "__main__":
    
    time.sleep(5)
    insert_employee_data_test(({'type': 'employee', 'name': "Martin", 'email': "Martin123@gmail.com", 'phoneNumber': "+16137075758"}))
    
    insert_customer_data_test(({'type': 'customer', 'name': "Jake", 'email': "Jake123@gmail.com", 'phoneNumber': "+16137075758"}))
    
    time.sleep(5)
    lcd_on_test()
    
    order_progress_test()
    
    customer_name_test(user_name_c)
    
    

