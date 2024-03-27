#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
import json
import socket
from time import sleep

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from . import IPService
from . import sauceService


# noinspection PyPep8
def parse_message(
    msg_code,
    sauce_level=2,
    msgType="TestCommunication",
    msgBody="Reply with Hi Pi3",
):
    # noinspection PyPep8
    """
    Parse incoming messages and form messages to send based on the provided msg_code.

    Args:
        msg_code (int): The code representing the type of message to parse.
        sauce_level (int, optional): The current sauce level. Defaults to 2.
        msgType (str, optional): The type of message to form. Defaults to "TestCommunication".
        msgBody (str, optional): The body of the message to form. Defaults to "Reply with Hi Pi3".

    Returns:
        str or dict or None: The parsed message or acknowledgment response, or None if the msg_code is invalid.
    """

    # From low sauce sms message to send to employee
    if msg_code == 0:
        low_sauce_message = (
            "Sauce level is critical! Current level is "
            + str(sauce_level)
            + ", please refill."
        )
        return low_sauce_message

    # Form ACK JSON reply to Pi2 after sauce dispensed
    elif msg_code == 1:
        return {"ACK": {"sender": "Pi3", "message": "complete"}}

    # Form JSON message to send via TCP
    elif msg_code == 2:
        return {msgType: {"sender": "Pi3", "message": msgBody}}

    # Incorrect msgCode
    else:
        print("Invalid message code")
        return None


# noinspection PyPep8
def send_message_then_receive_reply(piNum, msgType, msgBody):
    """
    Initialize environment to send a TCP message and receive a reply.

    Args:
        piNum (str): The number of the Pi to connect to.
        msgType (str): The type of message to send.
        msgBody (str): The body of the message to send.

    Returns:
        dict or None: The received acknowledgment response or None if no reply received or an error occurred.
    """

    host = IPService.get_ip(piNum)
    port = IPService.get_port(piNum)

    # Use these values instead if you're running the independent test
    # host = <your Pi's local ip address>
    # port = <your Pi's port number>

    timeout_seconds = 15

    pi3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    decoded_reply = None  # Initialize the variable

    try:
        pi3_socket.settimeout(timeout_seconds)  # Set socket timeout
        pi3_socket.connect((host, port))

        # Create the JSON message to send in the form of a dictionary
        message_json = parse_message(2, msgType=msgType, msgBody=msgBody)

        # Convert the dictionary to a JSON string
        message_str = json.dumps(message_json)

        # Send the JSON message to the server
        pi3_socket.sendall(message_str.encode("utf-8"))

        # Get ACK reply from the receiver
        raw_reply = pi3_socket.recv(1024)

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
        pi3_socket.close()

    # Return None if there was an error or timeout
    return decoded_reply if "decoded_reply" in locals() else None


# noinspection DuplicatedCode,PyPep8
def receive_message_then_reply(hostIp="0.0.0.0", portNum=53000):
    """
    Initialize environment to receive TCP messages from Pi2 and send an acknowledgment response.

    Args:
        hostIp (str, optional): The IP address to bind the socket to. Defaults to '0.0.0.0'.
        portNum (int, optional): The port number to listen on. Defaults to 53000.

    Returns:
        dict or None: The received message or None if an error occurred.
    """

    host = hostIp
    port = portNum

    # Create and bind a new socket for receiving
    pi3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi3_socket.bind((host, port))
    pi3_socket.listen(1)

    print(f"Pi3 listening on {host}:{port}")

    # Create a new socket for the incoming connection from Pi2
    pi2_socket, pi2_address = pi3_socket.accept()
    print(f"Connection established from Pi2 at {pi2_address}")

    received_msg = None  # Initialize variable

    try:
        # Wait for incoming message
        data = pi2_socket.recv(1024)
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

            # Check if customer choose to add sauce to their sandwich
            ordered_sauce = sauceService.get_ordered_sauce(orderNum)
            if ordered_sauce == "True":
                # Check if sauce level is low before dispensing
                sauce_level = sauceService.get_db_sauce_level()
                # If sauce level has reached zero, notify employee and wait for
                # refill before continuing
                if sauce_level <= 0:
                    print(
                        "Sauce has ran out, notifying and waiting for "
                        "employee to refill"
                    )
                    sauceService.notify_employee()
                    # ToDo get a specific employee number to pass on
                    sleep(5)
                    # ToDo better waiting mechanism
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
            pi2_socket.sendall(response_data.encode("utf-8"))
        else:
            print("Invalid JSON message structure received")

    # Print any socket errors that occur
    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the sockets
        pi3_socket.close()
        pi2_socket.close()

    return received_msg if "received_msg" in locals() else None


# noinspection PyPep8
def send_sms_message(msg_body, employee_phone):
    """
    Send an SMS notification to an employee using Twilio.

    Args:
        msg_body (str): The body of the SMS message to send.
        employee_phone (str): The phone number of the employee to whom the SMS will be sent.

    Returns:
        None

    Raises:
        TwilioRestException: If an error occurs during the Twilio API call.
    """

    # Setting Twilio API parameters and initializing a client
    # noinspection SpellCheckingInspection
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
