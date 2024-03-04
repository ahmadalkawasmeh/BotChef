import pyrebase

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

# Check the order info in Firebase and retrieve the customer's choice of sauce
def get_ordered_sauce():


# Dispense sauce by activating sauce pump
def dispense_sauce():


# Monitor sauce level
def check_sauce_level():


# Notify employee when sauce level is low
def notify_employee():

