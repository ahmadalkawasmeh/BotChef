from helperFunctions import IPService, messageService, toppingService

# Main program to run Pi#4 and delegate tasks to helper functions
def main():

    # Get my own IP address, I'm using Pi#4
    pi4_ip = IPService.get_local_ip_address(0)
    # Upload my Pi IP address to Firebase
    IPService.save_ip(pi4_ip)

    # Retrieve Pi#1 IP addresses
    pi1_ip = IPService.get_ip("Pi1")
    # Retrieve Pi#2 IP addresses
    pi2_ip = IPService.get_ip("Pi2")
    # Retrieve Pi#3 IP addresses
    pi3_ip = IPService.get_ip("Pi3")
    
if __name__ == "__main__":
    main()
