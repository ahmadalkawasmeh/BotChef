#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python

import unittest

from helperFunctions import messageService, IPService, sauceService
from testsHelperFunctions import unitHelper


class TestPi3(unittest.TestCase):
    """
    Unit tests for Raspberry Pi 3 functionalities.
    """

    def test_parse_low_sauce_message(self):
        """
        Test parsing low sauce message.
        """
        msg = "Sauce level is critical! Current level is 3, please refill."
        self.assertEqual(
            messageService.parse_message(msg_code=0, sauce_level=3), msg
        )

    def test_parse_reply_json_message(self):
        """
        Test parsing reply JSON message.
        """
        msg = {"ACK": {"sender": "Pi3", "message": "complete"}}
        self.assertEqual(messageService.parse_message(msg_code=1), msg)

    def test_parse_send_json_message(self):
        """
        Test parsing and sending JSON message.
        """
        msg = {"testType": {"sender": "Pi3", "message": "testBody"}}
        self.assertEqual(
            messageService.parse_message(
                msg_code=2, msgType="testType", msgBody="testBody"
            ),
            msg,
        )

    def test_get_port_Pi1(self):
        """
        Test getting port number for Pi1.
        """
        self.assertEqual(IPService.get_port("Pi1"), 51000)

    def test_get_port_Pi2(self):
        """
        Test getting port number for Pi2.
        """
        self.assertEqual(IPService.get_port("Pi2"), 52000)

    def test_get_port_Pi3(self):
        """
        Test getting port number for Pi3.
        """
        self.assertEqual(IPService.get_port("Pi3"), 53000)

    def test_get_port_Pi4(self):
        """
        Test getting port number for Pi4.
        """
        self.assertEqual(IPService.get_port("Pi4"), 54000)

    def test_get_ip_Pi3(self):
        """
        Test getting IP address for Pi3.
        """
        self.assertIsNotNone(IPService.get_ip("Pi3"))

    def test_save_and_get_ip(self):
        """
        Test saving and retrieving IP address.
        """
        local_ip = IPService.get_local_ip_address(0)
        IPService.save_ip(local_ip)
        self.assertEqual(IPService.get_ip("Pi3"), local_ip)

    def test_get_ordered_sauce(self):
        """
        Test getting ordered sauce.
        """
        self.assertEqual(sauceService.get_ordered_sauce(), "True")

    def test_get_employee_phone(self):
        """
        Test getting employee phone number.
        """
        self.assertEqual(sauceService.get_employee_phone(), "+16137075758")

    def test_update_sauce_level(self):
        """
        Test updating sauce level.
        """
        initial = sauceService.get_db_sauce_level()
        sauceService.update_sauce_level()
        self.assertEqual(sauceService.get_db_sauce_level(), initial - 1)

    def test_prox_sensor(self):
        """
        Test proximity sensor.
        """
        unitHelper.indicate_hardware_tst_started()
        unitHelper.sensor_wait(6)
        self.assertTrue(sauceService.sandwich_arrived())

    def test_sauce_pump(self):
        """
        Test sauce pump.
        """
        sauceService.sauce_dispenser(2)
        self.assertTrue(sauceService.sauce_dispenser(4))

    def test_ultrasonic_sensor(self):
        """
        Test ultrasonic sensor.
        """
        unitHelper.indicate_hardware_tst_ended()
        self.assertTrue(12.5 < sauceService.get_sauce_sensor_reading() < 16.5)


if __name__ == "__main__":
    unittest.main()
