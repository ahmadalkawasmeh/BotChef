#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python

from helperFunctions import IPService, messageService, sauceService


# Main program to run Pi#3 and delegate tasks to helper functions
def main():

    # Get my own IP address, I'm using Pi#3
    pi3_ip = IPService.get_local_ip_address(0)
    # Upload my Pi IP address to Firebase
    IPService.save_ip(pi3_ip)

    # Retrieve Pi#1 IP addresses
    pi1_ip = IPService.get_ip("Pi1")
    # Retrieve Pi#2 IP addresses
    pi2_ip = IPService.get_ip("Pi2")
    # Retrieve Pi#4 IP addresses
    pi4_ip = IPService.get_ip("Pi4")


