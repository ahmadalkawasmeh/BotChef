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


"""
This script provides functions to interact with Firebase and retrieve network information.

"""

# Retrieve my Pi's local IP address
def get_local_ip_address(n=0):
    
    """
    Retrieve the local IP address of the Raspberry Pi.

    Parameters:
        n (int): Determines the format of the IP address returned.
            - 0: Returns IP address as a string.
            - 1: Returns IP address within double quotes as a string.

    Returns:
        str: Local IP address of the Raspberry Pi.

    """
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
     """
    Upload the IP address of the Raspberry Pi to Firebase.

    Parameters:
        ip (str): IP address to be uploaded.

    """
    db.child("IPAddresses").child("Pi1").set(ip)

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
    """
    Retrieve the IP address of a specific Pi from Firebase.

    Parameters:
        piNum (str): The identifier of the Pi (e.g., "Pi1", "Pi2").

    Returns:
        str: IP address of the specified Pi.

    """
    stored_ip = (db.child("IPAddresses").child(piNum).get()).val()
    return stored_ip


# Return port numbers of other Pis
def get_port(piNum):
    
     """
    Return the port number associated with a specific Pi.

    Parameters:
        piNum (str): The identifier of the Pi (e.g., "Pi1", "Pi2").

    Returns:
        int: Port number of the specified Pi.

    """
    if piNum == "Pi3":
        return 53000

    elif piNum == "Pi2":
        return 52000

    elif piNum == "Pi4":
        return 54000

    else:
        print("Invalid piNum provided")
        return None
