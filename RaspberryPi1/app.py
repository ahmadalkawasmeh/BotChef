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
    x=db.child('Employee').child('IngredientsLevel').child('bread').get().val()
    x1=db.child('Employee').child('IngredientsLevel').child('lettuce').get().val()
    x2=db.child('Employee').child('IngredientsLevel').child('sauce').get().val()
    x3=db.child('Employee').child('IngredientsLevel').child('tomato').get().val()
    
    lcd.clear()
    return render_template('sandwichwebGUI.html', x=x, x1=x1, x2=x2, x3=x3)

@app.route('/submit', methods=['POST'])
def submit():
    
    data = request.form
    print("Received data:")
    json_data = {}
    for key, value in data.items():
        json_data[key] = value
    print(json_data)  
    
    lcd_on()
    
    
    if data.get('type') == 'customer':
        
        user_name_c=db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('customerName'))
        user_email_c=db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('customerEmail'))
        user_phone_c=db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('customerPhoneNumber'))
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('bread').set('True')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('sauce').set('True')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('tomato').set('True')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('lettuce').set('True')
        customer_name(user_name_c)
        customer_email(user_email_c)
        customer_phone(user_phone_c)
    
    
    if data.get('type') == 'employee':
        user_name_e = db.child('Employee').child('Employees').child('Employee1').child('name').set(data.get('employeeName'))
        user_email_e = db.child('Employee').child('Employees').child('Employee1').child('email').set(data.get('employeeEmail'))
        user_phone_e = db.child('Employee').child('Employees').child('Employee1').child('phone').set(data.get('employeePhoneNumber'))
        
        employee_name(user_name_e)
        employee_email(user_email_e)
        employee_phone(user_phone_e)
    
    
    order_progress()
    
        
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
        
        

def insert_customer_data(data):
    
    if data['type'] == 'customer':
        name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('name'))
        phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('phoneNumber'))
        email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('email'))
        
        name_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
        email_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
        phone_c_actual = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()

        
            

def insert_employee_data(data):
    
    if data['type'] == 'employee':
        name_e = db.child('Employee').child('Employees').child('Employee1').child('name').set(data.get('name'))
        email_e = db.child('Employee').child('Employees').child('Employee1').child('email').set(data.get('email'))
        phone_e = db.child('Employee').child('Employees').child('Employee1').child('phone').set(data.get('phoneNumber'))

        name_e_actual = db.child('Employee').child('Employees').child('Employee1').child('name').get().val()
        email_e_actual = db.child('Employee').child('Employees').child('Employee1').child('email').get().val()
        phone_e_actual = db.child('Employee').child('Employees').child('Employee1').child('phone').get().val()


def customer_name(user_name_c):
    orig_name_c = db.child('Customer').child('Order1').child('CustomerInfo').child('name').get().val()
    

def customer_email(user_email_c):
    orig_email_c = db.child('Customer').child('Order1').child('CustomerInfo').child('email').get().val()
    

def customer_phone(user_phone_c):
    orig_phone_c = db.child('Customer').child('Order1').child('CustomerInfo').child('phone').get().val()
    


def employee_name(user_name_e):
    orig_name_e = db.child('Employee').child('Order1').child('CustomerInfo').child('name').get().val()
        
    
def employee_email(user_email_e):
    orig_email_e = db.child('Employee').child('Order1').child('CustomerInfo').child('email').get().val()


def employee_phone(user_phone_e):
    orig_phone_e = db.child('Employee').child('Order1').child('CustomerInfo').child('phone').get().val()


def lcd_on():
    lcd = initialize_lcd()
    display_message(lcd, "On")

    
def order_progress():
    lcd = initialize_lcd()
    display_message(lcd, "start")
    time.sleep(10)
    display_message(lcd, "end")

    

def validate_user_inputs(data):
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
