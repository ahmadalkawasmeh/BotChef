#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
from time import time, sleep

import RPi.GPIO as GPIO


def sensor_wait(n=6):
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
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for LEDs
    green_led_pin = 16
    GPIO.setup(green_led_pin, GPIO.OUT)
    sleep(1)
    GPIO.output(green_led_pin, GPIO.HIGH)


def indicate_hardware_tst_ended():
    # Set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for LEDs
    green_led_pin = 16
    GPIO.setup(green_led_pin, GPIO.OUT)
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.cleanup()
