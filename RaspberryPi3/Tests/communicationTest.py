from RaspberryPi3.helperFunctions import messageService

# Test sending a message
def send_message_test():
    piNum = "Pi2"
    piPort = 52000
    msgType = "TestSignal"
    msgBody = "3/2"

    received_reply = messageService.send_message(piNum, piPort, msgType, msgBody)
    if "TestACK" in received_reply:
        result_calculation = received_reply["TestACK"]["message"]
        expected_result = 1.5
        actual_result = float(result_calculation)
        if expected_result == actual_result:
            print("send_message_test PASSED, expected: " + str(expected_result) + " , actual: " + str(actual_result))

        else:
            print("send_message_test FAILED, expected: " + str(expected_result) + " , actual: " + str(actual_result))
    else:
        print("TEST FAILED, Invalid reply message format received from " + piNum)



# Test receiving a message
def receive_message_test():


def save_ip_test():


def get_ip_test():

def get_ordered_sauce_test():


def check_sauce_level_test():


def update_sauce_level_test():


def get_employee_phone_test():
