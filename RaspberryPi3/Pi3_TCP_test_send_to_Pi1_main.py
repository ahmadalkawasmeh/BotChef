import communicationTest


# Runs the TCP test in communicationTests.py for sending a message then receiving a reply from receiver
def main():
    # Sending "3/1" to Pi1
    communicationTest.send_message_then_receive_reply_test(piNum="Pi1", msgType="TestSignal", msgBody="3/1")


if __name__ == "__main__":
    main()
