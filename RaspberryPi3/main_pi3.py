#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
from time import sleep

from helperFunctions import IPService, sauceService, messageService


def main():
    """
    Main program to run Pi#3 and delegate tasks to helper functions.

    This function initializes the Pi#3 environment, retrieves its IP address,
    uploads it to Firebase, initializes the sauce level in Firebase, and starts
    the sauce station.

    The function continuously listens for incoming messages using
    messageService.receive_message_then_reply(), and once a message is
    received, it processes the message and breaks the loop.
    """
    # Retrieve my IP address
    pi3_ip = IPService.get_local_ip_address(0)
    # Upload my IP address to Firebase
    IPService.save_ip(pi3_ip)

    # Initialize sauce level in Firebase
    sauceService.update_sauce_level()

    # Start sauce station, and wait for a message to arrive from Pi2
    while True:
        # Receive message and reply
        message = messageService.receive_message_then_reply()
        if message is not None:
            break
        # Wait for a short time before checking again
        sleep(2)


if __name__ == "__main__":
    main()
