import communicationTest


# Part 2 of the script used to test TCP messages independently at home. Make sure Part 1 is already running befpre
# executing this one!

# IMPORTANT make sure you've activated the VENV as you need to intall pyrebase, just activate the same venv
# you created in lab 3 then execute the scripts

# type 'source venv/bin/activate' in the terminal to activate

def main():
    communicationTest.send_message_then_receive_reply_test()


if __name__ == "__main__":
    main()