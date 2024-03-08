import communicationTest


# Runs the TCP test in communicationTests.py for sending a message then receiving a reply from receiver
def main():
    # Sending "3/2" to Pi2
    communicationTest.send_message_then_receive_reply_test()


if __name__ == "__main__":
    main()