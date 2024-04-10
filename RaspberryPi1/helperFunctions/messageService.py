import json
import socket
from time import sleep

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from . import IPService
#from . import sauceService



# Parse incoming messages and form messages to send
def parse_message(msg_code, sauce_level=2, msgType="TestCommunication", msgBody="Reply with Hi Pi2"):
     """
    Parse incoming messages and form messages to send based on the provided
    msg_code.

    Args:
        msg_code (int): The code representing the type of message to parse.
        sauce_level (int, optional): The current sauce level. Defaults to 2.
        msgType (str, optional): The type of message to form. Defaults
        to "TestCommunication".
        msgBody (str, optional): The body of the message to form. Defaults
        to "Reply with Hi Pi3".

    Returns:
        str: The sms message to send employee.
        dict: TCP message to send, or TCP ACK message.
        None: If the msg_code is invalid.
    """
    
    if msg_code == 0:
        low_sauce_message = 'Sauce level is critical! Current level is ' + str(sauce_level) + ', please refill.'
        return low_sauce_message

    elif msg_code == 1:
        return {"ACK": {"sender": "Pi1", "message": "complete"}}

    
    elif msg_code == 2:
        return {msgType: {"sender": "Pi1", "message": msgBody}}

    
    else:
        print("Invalid message code")
        return None



def send_message_then_receive_reply(piNum, msgType, msgBody):
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
    #host = IPService.get_ip(piNum)
    host='172.17.145.2'
    port=52000
    #port = IPService.get_port(piNum)
    timeout_seconds = 15

    pi1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    decoded_reply = None  # Initialize the variable

    try:
        pi1_socket.settimeout(timeout_seconds)  # Set socket timeout
        pi1_socket.connect((host, port))

        # Create the JSON message to send in the form of a dictionary
        message_json = parse_message(2, msgType=msgType, msgBody="Order1")

        # Convert the dictionary to a JSON string
        message_str = json.dumps(message_json)

        # Send the JSON message to the server
        pi1_socket.sendall(message_str.encode('utf-8'))

        # Get ACK reply from the receiver
        raw_reply = pi1_socket.recv(1024)

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
        pi1_socket.close()

    # Return None if there was an error or timeout
    return decoded_reply if 'decoded_reply' in locals() else None


# Initialize environment to receive TCP messages from Pi2
def receive_message_then_reply(hostIp='172.17.145.2', portNum=52000):
     """
    Initialize environment to receive TCP messages from Pi2 and send an
    acknowledgment response.

    Args:
        hostIp (str, optional): The IP address to bind the socket to. Defaults
        to '0.0.0.0'.
        portNum (int, optional): The port number to listen on. Defaults
        to 59000.

    Returns:
        dict: The received message
        None: If an error occurred.
    """

    host = hostIp
    port = portNum

    # Create and bind a new socket for receiving
    pi1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi1_socket.bind((host, port))
    pi1_socket.listen(1)

    print(f"Pi1 listening on {host}:{port}")

    # Create a new socket for the incoming connection from Pi2
    pi2_socket, pi2_address = pi1_socket.accept()
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
        pi1_socket.close()
        pi2_socket.close()

    return received_msg if 'received_msg' in locals() else None


# Send an SMS notification to employee
def send_sms_message(phone, msg_body):
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
