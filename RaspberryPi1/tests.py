   
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



def insert_employee_data_test(data):
    print("Beginning of database tests")
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
    print("Beginning of hardware tests")
    lcd = initialize_lcd()
    display_message(lcd, "On")

    try:
        assert get_message(lcd) == "On"
        print("Test passed: lcd_on")
    except AssertionError:
        print("Test failed")



lcd = initialize_lcd()
def order_progress_test():
    print("Beginning of software tests")
    lcd = initialize_lcd()
    display_message(lcd, "start")
    assert get_message(lcd) == "start"
    time.sleep(10)
    display_message(lcd, "end")
    assert get_message(lcd) == "end"


def customer_name_test(user_name_c):
    
    try:
        assert orig_name_c==user_name_c
        print("Test passed: customer name")
    except AssertionError:
        print("Test failed")


def customer_email_test(user_email_c):
   
    try:
        assert user_email_c == orig_email_c
        print("Test passed: customer email")
    except AssertionError:
        print("Test failed")

def customer_phone_test(user_phone_c):
    
    try:
        assert user_phone_c == orig_phone_c
        print("Test passed: customer phone")
    except AssertionError:
        print("Test failed")

def employee_name_test():
    try:
        assert user_name_e == orig_name_e
        print("Test passed: employee name")
    except AssertionError:
        print("Test failed")
        

def employee_email_test():
    try:
        assert user_email_e == orig_email_e
        print("Test passed: employee email")
    except AssertionError:
        print("Test failed")

def employee_phone_test():
    try:
        assert user_phone_e == orig_phone_e
        print("Test passed: employee phone")
    except AssertionError:
        print("Test failed")
    

        
def validate_customer_email(email):
    assert '@' in email

def validate_customer_phone(phone):
    assert phone.startswith('+1') and len(phone) == 12

def validate_employee_email(email):
    assert '@' in email

def validate_employee_phone(phone):
    assert phone.startswith('+1') and len(phone) == 12

