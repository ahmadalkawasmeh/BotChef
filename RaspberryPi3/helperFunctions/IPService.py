import netifaces as ni
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


# Retrieve my Pi's local IP address
def get_local_ip_address(n=1):
    try:
        my_ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        my_string_ip_address = f'"{my_ip_address}"'

        if n == 0:
            return my_ip_address
        if n == 1:
            return my_string_ip_address

    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None


# Upload IP address of my Raspberry Pi to Firebase
def save_ip(ip):
    db.child("IPAddresses").child("Pi3").set(ip)

    # The above command will add a JSON string to the Firebase in the form:
    # {
    #   "IPAddresses":{
    #     "Pi3":"<ip>"
    #   }
    # }
    #
    # and will also overwrite the previously stored ip address of my Raspberry Pi


# Retrieve IP of other Pis from Firebase
def get_ip(piNum):
    stored_ip = (db.child("IPAddresses").child(piNum).get()).val()
    return stored_ip 
