#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
import communicationTest

# Part 1 of the script used to test TCP messages independently at home, run this script first, then run the other one
def main():
    communicationTest.receive_message_then_reply_test()


if __name__ == "__main__":
    main()
