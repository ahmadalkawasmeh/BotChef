# Author: Ahmed
# Modified by: Zach
# This program deals with TCP messaging and SMS messaging for Pi2

import json
import socket
from time import sleep

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from . import IPRoutine
from . import actionsRoutine


def receive_message_then_reply(hostIp="0.0.0.0", portNum=52000) -> dict | None:
    """
    Initialize environment to receive TCP messages from Pi1 and send an
    acknowledgment response.

    Args:
        hostIp (str, optional): The IP address to bind the socket to. Defaults
        to '0.0.0.0'.
        portNum (int, optional): The port number to listen on. Defaults
        to 52000.

    Returns:
        dict: The received message
        None: If an error occurred.
    """

    host = hostIp
    port = portNum

    # Create and bind a new socket for receiving
    pi2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi2_socket.bind((host, port))
    pi2_socket.listen(1)

    print(f"Pi2 listening on {host}:{port}")

    # Create a new socket for the incoming connection from Pi2
    pi1_socket, pi1_address = pi2_socket.accept()
    print(f"Connection established from Pi1 at {pi1_address}")

    received_msg = None  # Initialize variable

    try:
        # Wait for incoming message
        data = pi1_socket.recv(1024)
        if not data:
            print("No data received")
            return None

        received_msg = json.loads(data.decode("utf-8"))
        print("Received JSON message: ")
        print(received_msg)

        # Check if the received message has the expected JSON structure
        if "Signal" in received_msg:
            sender = received_msg["Signal"]["sender"]
            message = received_msg["Signal"]["message"]
            orderNum = received_msg["Signal"]["orderNum"]

            #Try to dispense bread. Checking if there is any. 
            attempt_dispense()

            #Move belt
            actionsRoutine.move_belt(600, True)

            #Notify pi3
            #Send message and wait for reply
            send_message_then_receive_reply("Pi3", "Signal", message, orderNum)

            #Move belt
            actionsRoutine.move_belt(100, False)

            #Notify pi4
            #Send message and wait for reply
            send_message_then_receive_reply("Pi4", "Signal", message, orderNum)

            #Move belt
            actionsRoutine.move_belt(500, False)

            #Bread
            attempt_dispense()

            # Send an acknowledgment
            response_json = parse_message(1)
            response_data = json.dumps(response_json)
            pi1_socket.sendall(response_data.encode("utf-8"))
        else:
            print("Invalid JSON message structure received")

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the sockets
        pi2_socket.close()
        pi1_socket.close()

    return received_msg if "received_msg" in locals() else None


def parse_message(
    msg_code,
    bread_level=0,
    msgType="TestCommunication",
    msgBody="Reply with Hi Pi3",
    orderNum=0
) -> str | dict | None:
    """
    Parse incoming messages and form messages to send based on the provided
    msg_code.

    Args:
        msg_code (int): The code representing the type of message to parse.
        bread_level (int, optional): The current bread level. Defaults to 0.
        msgType (str, optional): The type of message to form. Defaults
        to "TestCommunication".
        msgBody (str, optional): The body of the message to form. Defaults
        to "Reply with Hi Pi3".

    Returns:
        str: The sms message to send employee.
        dict: TCP message to send, or TCP ACK message.
        None: If the msg_code is invalid.
    """

    # Form low bread sms message to send to employee
    if msg_code == 0:
        low_bread_message = (
            "Bread level is critical! Current level is "
            + str(bread_level)
            + ", please refill."
        )
        return low_bread_message

    # Form ACK JSON reply to Pi1 after sandwich made
    elif msg_code == 1:
        return {"ACK": {"sender": "Pi2", "message": "complete"}}

    # Form JSON message to send via TCP
    elif msg_code == 2:
        return {msgType: {"sender": "Pi2", "message": msgBody, "orderNum": orderNum}}

    # Incorrect msgCode
    else:
        print("Invalid message code")
        return None

  
def send_sms_message(msg_body, employee_phone) -> None:
    """
    Send an SMS notification to an employee using Twilio.

    Args:
        msg_body (str): The body of the SMS message to send.
        employee_phone (str): The phone number of the employee to whom the SMS
        will be sent.

    Returns:
        None

    Raises:
        TwilioRestException: If an error occurs during the Twilio API call.
    """

    # Setting Twilio API parameters and initializing a client
    account_sid = "AC8569b737cec74fdcbd0e6ede28ba4bc9"
    auth_token = "aa56f3a8083e9577ca17bbef42eb6e09"

    try:
        # Initializing Twilio client
        client = Client(account_sid, auth_token)

        # Sending an SMS message to employee
        message = client.messages.create(
            from_="+15177438114", body=msg_body, to=str(employee_phone)
        )

        print(f"SMS sent successfully. SID: {message.sid}")

    except TwilioRestException as e:
        print(f"Twilio error message: {e}")


def attempt_dispense():
    # Check if bread level is low before dispensing
    bread_level = actionsRoutine.get_db_bread_level()
    # If bread level is low, notify employee and wait for
    # refill before continuing
    if bread_level < 1:
        print(
            "Bread has ran out, notifying and waiting for "
            "employee to refill"
        )
        actionsRoutine.notify_employee()
        sleep(8)
        actionsRoutine.dispense_bread()
        sleep(1)
        actionsRoutine.update_bread_level()
    else:
        actionsRoutine.dispense_bread()
        actionsRoutine.update_bread_level()


def send_message_then_receive_reply(piNum, msgType, msgBody, orderNum) -> dict | None:
    """
    Initialize environment to send a TCP message and receive a reply.

    Args:
        piNum (str): The number of the Pi to connect to.
        msgType (str): The type of message to send.
        msgBody (str): The body of the message to send.

    Returns:
        dict: The received acknowledgment response.
        None: If no reply received or an error occurred.
    """

    host = IPRoutine.get_ip(piNum)
    port = IPRoutine.get_port(piNum)

    timeout_seconds = 15

    pi2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    decoded_reply = None  # Initialize the variable

    try:
        pi2_socket.settimeout(timeout_seconds)  # Set socket timeout
        pi2_socket.connect((host, port))

        # Create the JSON message to send in the form of a dictionary
        message_json = parse_message(2, msgType=msgType, msgBody=msgBody, orderNum=orderNum)

        # Convert the dictionary to a JSON string
        message_str = json.dumps(message_json)

        # Send the JSON message to the server
        pi2_socket.sendall(message_str.encode("utf-8"))

        # Get ACK reply from the receiver
        raw_reply = pi2_socket.recv(1024)

        # Handle partial or fragmented data
        if not raw_reply:
            print("No reply received")
            return None

        decoded_reply = json.loads(raw_reply.decode("utf-8"))
        print("Acknowledgment from " + piNum + " received with contents: ")
        print(decoded_reply)

    # If piNum takes too long to respond
    except socket.timeout:
        print(
            "Socket timout occurred, "
            + piNum
            + " didn't reply within 15 seconds"
        )

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    # Close socket
    finally:
        pi2_socket.close()

    # Return None if there was an error or timeout
    return decoded_reply if "decoded_reply" in locals() else None

