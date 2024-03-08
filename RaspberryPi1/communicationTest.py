from testsHelperFunctions import senseHatController
from helperFunctions import messageService, IPService, sauceService, login
import json
import socket
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


# Test TCP communication between Pi3 and Pi2, Pi3 sends a message to Pi2 containing a simple math calculation 3/2,
#  Pi2 performs the calculation and should reply with a message containing 1.5
#   Pi3 then checks the expected result against the actual received result and reports if the test Passes or Failed
def send_message_then_receive_reply_test(piNum="Pi2", msgType="TestSignal", msgBody="1/2"):

    received_reply = messageService.send_message_then_receive_reply(piNum, msgType, msgBody)

    if "TestACK" in received_reply:
        result_calculation = received_reply["TestACK"]["message"]
        actual_result = float(result_calculation)
        expected_result = 0.5

        if expected_result == actual_result:
            test_outcome = ("send_message_then_receive_reply_test() PASSED, expected: " + str(expected_result) +
                            " , actual: " + str(actual_result))

            print(test_outcome)
            senseHatController.sense_led("green", 2)
            senseHatController.sense_message(test_outcome)

        else:
            test_outcome = ("send_message_then_receive_reply_test() FAILED, expected: " +
                            str(expected_result) + " , actual: " + str(actual_result))

            print(test_outcome)
            senseHatController.sense_led("red", 2)
            senseHatController.sense_message(test_outcome)
    else:
        test_outcome = ("send_message_then_receive_reply_test() FAILED, Invalid reply message format received from " +
                        piNum)

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)


# Test receiving a message
def receive_message_then_reply_test(hostIp='0.0.0.0', portNum=51000):

    host = hostIp
    port = portNum

    # Create and bind a new socket for receiving
    pi3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi3_socket.bind((host, port))
    pi3_socket.listen(1)

    print(f"Pi3 listening on {host}:{port}")

    # Create a new socket for the incoming connection from Pi2
    sender_socket, sender_address = pi3_socket.accept()
    print(f"Connection established from Pi at {sender_address}")

    try:
        # Wait for incoming message
        data = sender_socket.recv(1024)
        if not data:
            print("No data received")
            return None

        received_msg = json.loads(data.decode('utf-8'))
        print("Received JSON message: ")
        print(received_msg)

        # Check if the received message has the expected JSON structure
        if "TestSignal" in received_msg:
            # Extract the requested calculation from JSON message
            requested_calculation = received_msg["TestSignal"]["message"]

            # Split the calculation request into two numbers
            parsed_calculation = requested_calculation.split("/")
            first_number = float(parsed_calculation[0])
            second_number = float(parsed_calculation[1])

            # Do the calculation
            calculation_result = first_number / second_number
            calculation_result_string = str(calculation_result)

            # Form the reply message
            response_json = messageService.parse_message(2, msgType="TestACK", msgBody=calculation_result_string)
            response_data = json.dumps(response_json)

            # Send the calculation result back
            sender_socket.sendall(response_data.encode('utf-8'))

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the sockets
        pi3_socket.close()
        sender_socket.close()


# Test uploading/retrieving my IP address to/from the Firebase. I first retrieve my local ip address via
#  IPService.get_local_ip_address(), then I upload it to the Firebase via IPService.save_ip(ip), then I
#   compare the two and ensure they are the same.
def save_and_get_ip_test():
    piNum = "Pi1"
    # Get my actual IP
    original_ip = IPService.get_local_ip_address()
    # Upload my IP to Firebase
    IPService.save_ip(original_ip)
    # Retrieve the IP address from Firebase
    firebase_ip = IPService.get_ip(piNum)

    # Compare the two and display result
    if firebase_ip == original_ip:
        test_outcome = ("save_and_get_ip_test() PASSED, expected: " + str(original_ip) +
                        " , actual: " + str(firebase_ip))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)

    else:
        test_outcome = ("save_and_get_ip_test() FAILED, expected: " + str(original_ip) +
                        " , actual: " + str(firebase_ip))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)





# Test retrieving employee phone number from Firebase. First I will overwrite the phone number in Firebase with
#  +16137075758 , then I will retrieve and compare it to the original phone number
def get_employee_phone_test():
    employeeNum = "Employee1"
    set_employee_phone = "+16137075758"

    db.child("Employee").child("Employees").child(employeeNum).child("phone").set(set_employee_phone)
    firebase_employee_phone = sauceService.get_employee_phone(employeeNum)

    if set_employee_phone == firebase_employee_phone:
        test_outcome = ("get_employee_phone_test() PASSED, expected: " + str(set_employee_phone) +
                        " , actual: " + str(firebase_employee_phone))
        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)

    else:
        test_outcome = ("get_employee_phone_test() FAILED, expected: " + str(set_employee_phone) +
                        " , actual: " + str(firebase_employee_phone))
        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)

def get_customer_name_test():
    orderNum = "Order1"
    original_customer_name='jake'
    db.child("Customer").child(orderNum).child("CustomerInfo").child("name").set(original_customer_name)
    firebase_customer_name= login.get_customer_name(orderNum)
    if original_customer_name == firebase_customer_name:
        test_outcome = ("get_customer_name_test() PASSED, expected: " + str(original_customer_name) +
                        " , actual: " + str(firebase_customer_name))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("name").set("True")

    else:
        test_outcome = ("get_customer_name_test() FAILED, expected: " + str(original_customer_name) +
                        " , actual: " + str(firebase_customer_name))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("name").set("True")


# Test decrementing sauce the sauce level when dispensed. I will firstly overwrite the sauce level in Firebase with
#  5, then I will invoke sauceService.update_sauce_level(1) to decrement it by 1, then I will compare the expected
#   sauce level which is 4 to the actual retrieved value
def get_customer_email_test():
    orderNum="Order1"
    original_customer_email='jake123@gmail.com'

    db.child("Customer").child(orderNum).child("CustomerInfo").child("email").set(original_customer_email)
    firebase_customer_email= login.get_customer_email(orderNum)
    if original_customer_email == firebase_customer_email:
        test_outcome = ("get_customer_email_test() PASSED, expected: " + str(original_customer_email) +
                        " , actual: " + str(firebase_customer_email))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("email").set("True")

    else:
        test_outcome = ("get_customer_email_test() FAILED, expected: " + str(original_customer_email) +
                        " , actual: " + str(firebase_customer_email))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("email").set("True")


# Test retrieving employee phone number from Firebase. First I will overwrite the phone number in Firebase with
#  +16137075758 , then I will retrieve and compare it to the original phone number
def get_customer_phone_test():
    orderNum="Order1"
    original_customer_phone='+16137075758'

    db.child("Customer").child(orderNum).child("CustomerInfo").child("phone").set(original_customer_phone)
    firebase_customer_phone= firebase.get_customer_phone(orderNum)
    if original_customer_phone == firebase_customer_phone:
        test_outcome = ("get_customer_phone_test() PASSED, expected: " + str(original_customer_phone) +
                        " , actual: " + str(firebase_customer_phone))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("phone").set("True")

    else:
        test_outcome = ("get_customer_phone_test() FAILED, expected: " + str(original_customer_phone) +
                        " , actual: " + str(firebase_customer_phone))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("CustomerInfo").child("phone").set("True")

def get_employee_name_test():
    original_employee_name='Martin'

    db.child("Employee").child("Employees").child("Employee1").child("name").set(original_employee_name)
    firebase_employee_name= login.get_employee_name()
    if original_employee_name == firebase_employee_name:
        test_outcome = ("get_employee_name_test() PASSED, expected: " + str(original_employee_name) +
                        " , actual: " + str(firebase_employee_name))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("name").set("True")

    else:
        test_outcome = ("get_employee_name_test() FAILED, expected: " + str(original_employee_name) +
                        " , actual: " + str(firebase_employee_name))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("name").set("True")

# Test decrementing sauce the sauce level when dispensed. I will firstly overwrite the sauce level in Firebase with
#  5, then I will invoke sauceService.update_sauce_level(1) to decrement it by 1, then I will compare the expected
#   sauce level which is 4 to the actual retrieved value
def get_employee_email_test():
    original_employee_email='Martin123@gmail.com'

    db.child("Employee").child("Employees").child("Employee1").child("email").set(original_employee_email)
    firebase_employee_email= login.get_employee_email()
    if original_employee_email == firebase_employee_email:
        test_outcome = ("get_employee_email_test() PASSED, expected: " + str(original_employee_email) +
                        " , actual: " + str(firebase_employee_email))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("email").set("True")

    else:
        test_outcome = ("get_employee_email_test() FAILED, expected: " + str(original_employee_email) +
                        " , actual: " + str(firebase_employee_email))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("email").set("True")


# Test retrieving employee phone number from Firebase. First I will overwrite the phone number in Firebase with
#  +16137075758 , then I will retrieve and compare it to the original phone number
def get_employee_phone_test():
    original_employee_phone='+16137075758'

    db.child("Employee").child("Employees").child("Employee1").child("phone").set(original_employee_phone)
    firebase_employee_phone= login.get_employee_phone()
    if original_employee_phone == firebase_employee_phone:
        test_outcome = ("get_employee_phone_test() PASSED, expected: " + str(original_employee_phone) +
                        " , actual: " + str(firebase_employee_phone))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("phone").set("True")

    else:
        test_outcome = ("get_employee_phone_test() FAILED, expected: " + str(original_employee_phone) +
                        " , actual: " + str(firebase_employee_phone))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Employee").child("Employees").child("Employee1").child("phone").set("True")
