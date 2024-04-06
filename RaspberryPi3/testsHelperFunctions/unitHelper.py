#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
"""
Module for controlling hardware testing functions using GPIO on Raspberry Pi.
"""

from time import time, sleep
import RPi.GPIO as GPIO


def sensor_wait(n=6):
    """
    Cycle an LED for a specified duration.

    Parameters: n (int): The duration of the LED cycling in seconds. Default
    is 6 seconds.
    """
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for LEDs
    red_led_pin = 20
    GPIO.setup(red_led_pin, GPIO.OUT)
    cycle_duration = n  # in seconds

    try:
        # Start cycling the LED
        start_time = time()
        while time() - start_time < cycle_duration:
            # Turn the LED on
            GPIO.output(red_led_pin, GPIO.HIGH)
            sleep(0.5)  # LED on for 0.5 seconds

            # Turn the LED off
            GPIO.output(red_led_pin, GPIO.LOW)
            sleep(0.5)  # LED off for 0.5 seconds

    finally:
        # Clean up GPIO
        GPIO.cleanup()


def indicate_hardware_tst_started():
    """
    Indicate the start of hardware testing by turning on a green LED.
    """
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for LEDs
    green_led_pin = 16
    GPIO.setup(green_led_pin, GPIO.OUT)
    sleep(1)
    GPIO.output(green_led_pin, GPIO.HIGH)


def indicate_hardware_tst_ended():
    """
    Indicate the end of hardware testing by turning off a green LED and
    cleaning up GPIO.
    """
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for LEDs
    green_led_pin = 16
    GPIO.setup(green_led_pin, GPIO.OUT)
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.cleanup()
