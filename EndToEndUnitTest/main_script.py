import pyrebase
from flask import Flask, render_template, request, request
import pyrebase
from flask_socketio import SocketIO
import time
import RPi.GPIO as GPIO
from RPLCD import CharLCD
from display import initialize_lcd, display_message, get_message
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


app = Flask(__name__)
socketio = SocketIO(app)


#Firebase configuration

config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
dataset = "orderdata"
username = "webGUI"


app = Flask(__name__)

lcd=initialize_lcd()

@app.route('/')
def index():
    lcd.clear()
    return render_template('sandwichwebGUI.html')

@app.route('/submit', methods=['POST'])
def submit():
    
    data = request.form
    print("Received data:")
    json_data = {}
    for key, value in data.items():
        json_data[key] = value
    print(json_data)  
    
    lcd_on_test()
    
    
    if data.get('type') == 'customer':
        
        user_name_c=db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('customerName'))
        user_email_c=db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('customerEmail'))
        user_phone_c=db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('customerPhoneNumber'))
        
        customer_name_test(user_name_c)
        customer_email_test(user_email_c)
        customer_phone_test(user_phone_c)
    
    
    if data.get('type') == 'employee':
        user_name_e = db.child('Employee').child('Employees').child('Employee1').child('name').set(data.get('employeeName'))
        user_email_e = db.child('Employee').child('Employees').child('Employee1').child('email').set(data.get('employeeEmail'))
        user_phone_e = db.child('Employee').child('Employees').child('Employee1').child('phone').set(data.get('employeePhoneNumber'))
        
        employee_name_test(user_name_e)
        employee_email_test(user_email_e)
        employee_phone_test(user_phone_e)
    
    if data.get('type') == 'ingredients':
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').set(data.get('breadSelected'))
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').set(data.get('sauceSelected'))
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').set(data.get('lettuceSelected'))
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').set(data.get('tomatoSelected'))
    
    order_progress_test()
    
        
    return 'Order receieved thank you'


    
def send_sms_message(employeePhoneNumber, msg_body="order done"):
    # Setting Twilio API parameters and initializing a client
    account_sid = 'AC8569b737cec74fdcbd0e6ede28ba4bc9'
    auth_token = 'aa56f3a8083e9577ca17bbef42eb6e09'

    try:
        # Initializing Twilio client
        client = Client(account_sid, auth_token)

        # Sending an SMS message to employee
        message = client.messages.create(
            from_='+15177438114',
            body=msg_body,
            to=str(employeePhoneNumber)
        )

        print(f"SMS sent successfully. SID: {message.sid}")

    except TwilioRestException as e:
        print(f"Twilio error message: {e}")
        
        

def insert_customer_data_test(data):
    print("Beginning of database tests")
    if data['type'] == 'customer':
        name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('name'))
        phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('phoneNumber'))
        email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('email'))
        
        name_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
        email_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
        phone_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()

        try:
            assert name_c == name_c_actual
            print("Test passed: customer name")
        except AssertionError:
            print("Test failed")

        try:
            assert email_c == email_c_actual
            print("Test passed: customer email")
        except AssertionError:
            print("Test failed")

        try:
            assert phone_c == phone_c_actual
            print("Test passed: customer phone")
        except AssertionError:
            print("Test failed")
            
            

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
            print("Test passed: employee name")
        except AssertionError:
            print("Test failed")

        try:
            assert email_e == email_e_actual
            print("Test passed: employee email")
        except AssertionError:
            print("Test failed")

        try:
            assert phone_e == phone_e_actual
            print("Test passed: employee phone")
        except AssertionError:
            print("Test failed")





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
        


def employee_name_test(user_name_e):
    orig_name_e = db.child('Employee').child('Order1').child('CustomerInfo').child('name').get().val()
    
    try:
        assert user_name_e == orig_name_e
        print("Test passed: employee name")
    except AssertionError:
        print("Test failed")
        
        
    

def employee_email_test(user_email_e):
    orig_email_e = db.child('Employee').child('Order1').child('CustomerInfo').child('email').get().val()
    try:
        assert user_email_e == orig_email_e
        print("Test passed: employee email")
    except AssertionError:
        print("Test failed")

def employee_phone_test(user_phone_e):
    orig_phone_e = db.child('Employee').child('Order1').child('CustomerInfo').child('phone').get().val()
    try:
        assert user_phone_e == orig_phone_e
        print("Test passed: employee phone")
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



def order_progress_test():
    lcd = initialize_lcd()
    display_message(lcd, "start")
    assert get_message(lcd) == "start"
    time.sleep(10)
    display_message(lcd, "end")
    assert get_message(lcd) == "end"
    

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
    assert '@' in email

def assert_customer_phone(phone):
    assert phone.startswith('+1') and len(phone) == 12

def assert_employee_email(email):
    assert '@' in email



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
    customer_name_test()
    
