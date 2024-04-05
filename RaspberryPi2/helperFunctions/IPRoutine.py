import netifaces as ni
import pyrebase


# Firebase connection
config = {
    "apiKey": "AIzaSyC3QNNa52-lh5JimhS0zgC0sA_z6XUq3JY",
    "authDomain": "sysc3010-f898a.firebaseapp.com",
    "databaseURL": "https://sysc3010-f898a-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f898a.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_local_ip_address(n=1) -> str | None:
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
        my_ip_address = ni.ifaddresses("wlan0")[ni.AF_INET][0]["addr"]
        my_string_ip_address = f'"{my_ip_address}"'

        if n == 0:
            return my_ip_address
        if n == 1:
            return my_string_ip_address

    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def save_ip(ip) -> None:
    """
    Upload the IP address of the Raspberry Pi to Firebase.

    Parameters:
        ip (str): IP address to be uploaded.

    """
    db.child("IPAddresses").child("Pi2").set(ip)

def get_ip(piNum) -> str:
    """
    Retrieve the IP address of a specific Pi from Firebase.

    Parameters:
        piNum (str): The identifier of the Pi (e.g., "Pi1", "Pi2").

    Returns:
        str: IP address of the specified Pi.

    """
    stored_ip = (db.child("IPAddresses").child(piNum).get()).val()
    return stored_ip

def get_port(piNum) -> int | None:
    """
    Return the port number associated with a specific Pi.

    Parameters:
        piNum (str): The identifier of the Pi (e.g., "Pi1", "Pi2").

    Returns:
        int: Port number of the specified Pi.

    """
    if piNum == "Pi1":
        return 51000

    elif piNum == "Pi2":
        return 52000

    elif piNum == "Pi3":
        return 53000

    elif piNum == "Pi4":
        return 54000

    else:
        print("Invalid piNum provided")
        return None
