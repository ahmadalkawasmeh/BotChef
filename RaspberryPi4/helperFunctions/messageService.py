import json
import socket
from time import sleep

# from twilio.base.exceptions import TwilioRestException
# from twilio.rest import Client

from . import IPService
from . import toppingService


# Parse incoming messages and form messages to send
def parse_message(msg_code, topping_level=2, msgType="TestCommunication", msgBody="Reply with Hi Pi4"):
    # From low sauce sms message to send to employee
    if msg_code == 0:
        low_sauce_message = 'Sauce level is critical! Current level is ' + str(sauce_level) + ', please refill.'
        return low_sauce_message

    # Form ACK JSON reply to Pi2 after sauce dispensed
    elif msg_code == 1:
        return {"ACK": {"sender": "Pi4", "message": "complete"}}

    # Form JSON message to send via TCP
    elif msg_code == 2:
        return {msgType: {"sender": "Pi4", "message": msgBody}}

    # Incorrect msgCode
    else:
        print("Invalid message code")
        return None


# Initialize environment to send a TCP message
def send_message_then_receive_reply(piNum, msgType, msgBody):
    #host = IPService.get_ip(piNum)
    host = '192.168.2.76'
    #port = IPService.get_port(piNum)
    port = 54000

    # Use these values instead if you're running the independent test
    # host = <your Pi's local ip address>
    # port = <your Pi's port number>

    timeout_seconds = 15

    pi4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    decoded_reply = None  # Initialize the variable

    try:
        pi4_socket.settimeout(timeout_seconds)  # Set socket timeout
        pi4_socket.connect((host, port))

        # Create the JSON message to send in the form of a dictionary
        message_json = parse_message(2, msgType=msgType, msgBody=msgBody)

        # Convert the dictionary to a JSON string
        message_str = json.dumps(message_json)

        # Send the JSON message to the server
        pi4_socket.sendall(message_str.encode('utf-8'))

        # Get ACK reply from the receiver
        raw_reply = pi4_socket.recv(1024)

        # Handle partial or fragmented data
        if not raw_reply:
            print("No reply received")
            return None

        decoded_reply = json.loads(raw_reply.decode('utf-8'))
        print("Acknowledgment from " + piNum + " received with contents: ")
        print(decoded_reply)

    # If piNum takes too long to respond
    except socket.timeout:
        print("Socket timout occurred, " + piNum + " didn't reply within 15 seconds")

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    # Close socket
    finally:
        pi4_socket.close()

    # Return None if there was an error or timeout
    return decoded_reply if 'decoded_reply' in locals() else None


# Initialize environment to receive TCP messages from Pi2
def receive_message_then_reply(hostIp='0.0.0.0', portNum=54000):
    host = hostIp
    port = portNum

    # Create and bind a new socket for receiving
    pi4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi4_socket.bind((host, port))
    pi4_socket.listen(1)

    print(f"Pi4 listening on {host}:{port}")

    # Create a new socket for the incoming connection from Pi2
    pi2_socket, pi2_address = pi4_socket.accept()
    print(f"Connection established from Pi2 at {pi2_address}")

    received_msg = None  # Initialize variable

    try:
        # Wait for incoming message
        data = pi2_socket.recv(1024)
        if not data:
            print("No data received")
            return None

        received_msg = json.loads(data.decode('utf-8'))
        print("Received JSON message: ")
        print(received_msg)

        # Check if the received message has the expected JSON structure
        if "Signal" in received_msg:
            sender = received_msg["Signal"]["sender"]
            message = received_msg["Signal"]["message"]
            orderNum = received_msg["Signal"]["orderNum"]

            # Check if customer choose to add sauce to their sandwich
            ordered_sauce = sauceService.get_ordered_sauce(orderNum)
            if ordered_sauce == "True":
                # Check if sauce level is low before dispensing
                sauce_level = sauceService.get_db_sauce_level()
                # If sauce level has reached zero, notify employee and wait for refill before continuing
                if sauce_level <= 0:
                    print("Sauce has ran out, notifying and waiting for employee to refill")
                    sauceService.notify_employee()  # ToDo get a specific employee number to pass on
                    sleep(5)  # ToDo better waiting mechanism
                    sauceService.dispense_sauce(ordered_sauce)
                    sauceService.update_sauce_level()
                else:
                    sauceService.dispense_sauce(ordered_sauce)
                    sauceService.update_sauce_level()
            else:
                sauceService.dispense_sauce(ordered_sauce)

            # Send an acknowledgment
            response_json = parse_message(1)
            response_data = json.dumps(response_json)
            pi2_socket.sendall(response_data.encode('utf-8'))
        else:
            print("Invalid JSON message structure received")

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the sockets
        pi4_socket.close()
        pi2_socket.close()

    return received_msg if 'received_msg' in locals() else None


# # Send an SMS notification to employee
# def send_sms_message(msg_body, employee_phone):
#     # Setting Twilio API parameters and initializing a client
#     account_sid = 'AC8569b737cec74fdcbd0e6ede28ba4bc9'
#     auth_token = 'aa56f3a8083e9577ca17bbef42eb6e09'
# 
#     try:
#         # Initializing Twilio client
#         client = Client(account_sid, auth_token)
# 
#         # Sending an SMS message to employee
#         message = client.messages.create(
#             from_='+15177438114',
#             body=msg_body,
#             to=str(employee_phone)
#         )
# 
#         print(f"SMS sent successfully. SID: {message.sid}")
# 
#     except TwilioRestException as e:
#         print(f"Twilio error message: {e}")
