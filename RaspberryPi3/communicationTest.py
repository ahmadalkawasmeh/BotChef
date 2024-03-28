#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
import json
import socket

import pyrebase

from helperFunctions import messageService, IPService, sauceService
from testsHelperFunctions import senseHatController

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
def send_message_then_receive_reply_test(piNum="Pi2", msgType="TestSignal", msgBody="3/2"):

    received_reply = messageService.send_message_then_receive_reply(piNum, msgType, msgBody)

    if "TestACK" in received_reply:
        result_calculation = received_reply["TestACK"]["message"]
        actual_result = float(result_calculation)

        parsed_calculation = msgBody.split("/")
        first_number = float(parsed_calculation[0])
        second_number = float(parsed_calculation[1])
        expected_result = first_number / second_number

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
def receive_message_then_reply_test(hostIp='0.0.0.0', portNum=53000):
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
    piNum = "Pi3"
    # Get my actual IP
    original_ip = IPService.get_local_ip_address(0)
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


# Test retrieving sauce choice from customer's order. I first set the order sauce choice to "False" in
#  the Firebase, then I will retrieve it and make sure the value I set is the same as the retrieved value.
#   Then at the end I'll update the sauce choice to "True"
def get_ordered_sauce_test():
    orderNum = "Order1"
    original_sauce_choice = "False"
    db.child("Customer").child(orderNum).child("OrderInfo").child("Ingredients").child("sauce").set(
        original_sauce_choice)
    firebase_sauce_choice = sauceService.get_ordered_sauce(orderNum)
    if original_sauce_choice == firebase_sauce_choice:
        test_outcome = ("get_ordered_sauce_test() PASSED, expected: " + str(original_sauce_choice) +
                        " , actual: " + str(firebase_sauce_choice))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("OrderInfo").child("Ingredients").child("sauce").set("True")

    else:
        test_outcome = ("get_ordered_sauce_test() FAILED, expected: " + str(original_sauce_choice) +
                        " , actual: " + str(firebase_sauce_choice))

        print(test_outcome)
        senseHatController.sense_led("red", 2)
        senseHatController.sense_message(test_outcome)
        db.child("Customer").child(orderNum).child("OrderInfo").child("Ingredients").child("sauce").set("True")


# Test decrementing sauce the sauce level when dispensed. I will firstly overwrite the sauce level in Firebase with
#  5, then I will invoke sauceService.update_sauce_level(1) to decrement it by 1, then I will compare the expected
#   sauce level which is 4 to the actual retrieved value
def update_sauce_level_test():
    set_sauce_level = 5

    db.child("Employee").child("IngredientsLevel").child("sauce").set(set_sauce_level)
    sauceService.update_sauce_level(1)

    expected_sauce_level = set_sauce_level - 1
    actual_sauce_level = sauceService.get_db_sauce_level()

    if expected_sauce_level == actual_sauce_level:
        test_outcome = ("update_sauce_level_test() PASSED, expected: " + str(expected_sauce_level) +
                        " , actual: " + str(actual_sauce_level))

        print(test_outcome)
        senseHatController.sense_led("green", 2)
        senseHatController.sense_message(test_outcome)
    else:
        test_outcome = ("update_sauce_level_test() FAILED, expected: " + str(expected_sauce_level) +
                        " , actual: " + str(actual_sauce_level))

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
