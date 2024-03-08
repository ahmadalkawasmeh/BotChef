import communicationTest


# Runs the TCP test in communicationTests.py for receiving a message then replying to sender
def main():
    communicationTest.receive_message_then_reply_test()


if __name__ == "__main__":
    main()