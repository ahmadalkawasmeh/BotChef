# Author: Zach Gregory
# Run this program to begin operation of RPi #2

#python3 -m venv .venv
#source .venv/bin/activate
#python3 /home/zach/Desktop/main_pi2.py

from time import sleep
from helperFunctions import IPRoutine, actionsRoutine, messagingRoutine


def main():
    # Retrieve my IP address
    pi2_ip = IPRoutine.get_local_ip_address(0)
    # Upload my IP address to Firebase
    IPRoutine.save_ip(pi2_ip)

    # Initialize bread level in Firebase
    actionsRoutine.update_bread_level()

    # Wait for a message to arrive from Pi1
    while True:
        # Receive message and reply (replies after sandwich is complete)
        message = messagingRoutine.receive_message_then_reply()
        if message is not None:
            break
        # Wait for a short time before checking again
        sleep(2)


if __name__ == "__main__":
    main()
