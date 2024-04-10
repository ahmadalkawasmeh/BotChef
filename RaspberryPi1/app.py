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
from helperFunctions import IPService, messageService

"""Module for running flask and accessing web GUI order site."""

#initalzing socket
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
    """Render template with ingredient levels retrieved from the database."""
    x=db.child('Employee').child('IngredientsLevel').child('bread').get().val() #bread
    x2=db.child('Employee').child('IngredientsLevel').child('lettuce').get().val() #lettuce
    x1=db.child('Employee').child('IngredientsLevel').child('sauce').get().val() #sauce
    x3=db.child('Employee').child('IngredientsLevel').child('tomato').get().val() #tomato
    
    lcd.clear() #clear LCD everytime website is refreshed
    return render_template('sandwichwebGUI.html', x=x, x1=x1, x2=x2, x3=x3)


#submit function to get the data from the GUI once an order is placed
@app.route('/submit', methods=['POST']) 
def submit():
    """Process the data from the GUI once an order is placed."""
    data = request.form
    print("Received data:")
    sandwich_data= {} #store data as JSON
    for key, value in data.items():
        sandwich_data[key] = value
    print(sandwich_data)  #print data in the console
    
    
    if data.get('type') == 'customer':  #checks if a customer placed an order
        
        user_name_c=db.child('Customer').child('Order1').child('CustomerInfo').child('name').set(data.get('customerName')) #sets the customer name in db
        user_email_c=db.child('Customer').child('Order1').child('CustomerInfo').child('email').set(data.get('customerEmail')) #sets the customer email in db
        user_phone_c=db.child('Customer').child('Order1').child('CustomerInfo').child('phone').set(data.get('customerPhoneNumber')) #sets the customer phone in db
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('bread').set('True')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('sauce').set('True')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('tomato').set('False')
        db.child('Customer').child('Order1').child('OrderInfo').child('Ingredients').child('lettuce').set('True')
        
        customerPhoneNumber = data.get('customerPhoneNumber')  
        send_sms_message(customerPhoneNumber, ) #sends the sms message to customer confirming their order is placed
        
        order_start() #function call to display start message on the LCD
        
        message=messageService.send_message_then_receive_reply("Pi2","Signal", "start order") #sends TCP message to Pi2 to start the order
        
        return 'Order receieved, thank you. You will be notified when the order is ready'
        
        wait_for_order
        
        
       
        
    if data.get('type') == 'employee': #checks if an employee entered their credentials
        user_name_e = db.child('Employee').child('Employees').child('Employee1').child('name').set(data.get('employeeName')) #sets employee name in db
        user_email_e = db.child('Employee').child('Employees').child('Employee1').child('email').set(data.get('employeeEmail')) #sets employee email in db
        user_phone_e = db.child('Employee').child('Employees').child('Employee1').child('phone').set(data.get('employeePhoneNumber')) #sets employee phone number in db
        
        
    
        return 'Employee credentials noted, you will be notified if ingredients levels run low'
    
    
    


def wait_for_order():
    """Wait for orders and delegate tasks to helper functions."""
    
    pi1_ip = IPService.get_local_ip_address(0)
    IPService.save_ip(pi1_ip)
    

    while True:
        message=messageService.receive_message_then_reply()
        customerphone=get_customer_phone()
        send_sms_message(customerphone,"order done")
        order_done()
        return 'Order ready!'
        break
    sleep(2)
        


def get_customer_phone():
    """Retrieve customer phone number from submitted data."""

    return data.get('customerPhoneNumber')
    

def send_sms_message(phone, msg_body="order placed succesfully"): 
    """Send an SMS confirmation message to the provided phone number."""

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
            to=str(phone)
        )

        print(f"SMS sent successfully. SID: {message.sid}")

    except TwilioRestException as e:
        print(f"Twilio error message: {e}")
        
        

def lcd_on():
    """Display on message on the LCD."""

    lcd = initialize_lcd()
    display_message(lcd, "On")

    
def order_start():
    """Display start message on the LCD."""

    lcd = initialize_lcd()
    display_message(lcd, "start")
    
def order_done():
    """Display end message on the LCD."""

    lcd = initialize_lcd()
    display_message(lcd, "end")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
    
