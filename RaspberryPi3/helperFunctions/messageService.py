from twilio.rest import Client

# Parse incoming messages and form messages to send
def parse_message(msg_code, sauce_level = 2):
    if msg_code == 0:
        # From low sauce sms message to employee
        low_sauce_message = 'Sauce level is critical! Current level is ' + str(sauce_level) + ', please refill.'
        return low_sauce_message


# Initialize environment to send a TCP message
def send_message():


# Initialize environment to receive TCP messages
def recieve_message():


# Send an SMS notification to employee
def send_smsMessage(message, employee_phone):
    # Setting Twilio API parameters and initializing a client
    account_sid = 'AC8569b737cec74fdcbd0e6ede28ba4bc9'
    auth_token = 'aa56f3a8083e9577ca17bbef42eb6e09'
    client = Client(account_sid, auth_token)

    # Sending an sms message to employee
    message = client.messages.create(
        from_='+15177438114',
        body= message,
        to= str(employee_phone)
    )
