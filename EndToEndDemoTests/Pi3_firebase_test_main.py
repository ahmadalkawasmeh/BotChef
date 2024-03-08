import communicationTest


# Runs all the firebase tests in communicationTests.py
def main():
    communicationTest.save_and_get_ip_test()
    communicationTest.get_ordered_sauce_test()
    communicationTest.update_sauce_level_test()
    communicationTest.get_employee_phone_test()


if __name__ == "__main__":
    main()
