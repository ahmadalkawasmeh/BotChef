from helperFunctions import IPService, messageService, sauceService
import communicationTest


# Main program to run Pi#1 and delegate tasks to helper functions
def main():
    # Get my own IP address, I'm using Pi#1
    pi1_ip = IPService.get_local_ip_address(0)
    # Upload my Pi IP address to Firebase
    IPService.save_ip(pi1_ip)

    # Retrieve Pi#3 IP addresses
    pi3_ip = IPService.get_ip("Pi3")
    # Retrieve Pi#2 IP addresses
    pi2_ip = IPService.get_ip("Pi2")
    # Retrieve Pi#4 IP addresses
    pi4_ip = IPService.get_ip("Pi4")
    
    
    
    
    #communicationTest.send_message_then_receive_reply_test()
    #communicationTest.receive_message_then_reply_test()
    communicationTest.save_and_get_ip_test()
    communicationTest.get_customer_name_test()
    communicationTest.get_customer_email_test()
    communicationTest.get_customer_phone_test()
    communicationTest.get_employee_name_test()
    communicationTest.get_employee_email_test()
    communicationTest.get_employee_phone_test()


if __name__== "__main__":
    main()
