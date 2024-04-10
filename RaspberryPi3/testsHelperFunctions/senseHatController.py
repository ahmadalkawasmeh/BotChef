#!/home/koko/Documents/sysc3010-project-l2-g12/RaspberryPi3/venv/bin/python
"""
Module for controlling the Sense HAT LEDs and displaying messages.
"""

from time import sleep
from sense_hat import SenseHat

# Initialize the Sense HAT
sense = SenseHat()


def sense_led(color, t=5):
    """
    Set the LEDs to red or green for a specified duration.

    Parameters: color (str): The color to set the LEDs to, either "red" or
    "green". t (int): The duration in seconds for which to display the
    color. Default is 5 seconds.
    """
    if color == "red":
        # Set all pixels to red
        sense.clear((127, 0, 0))

        # Wait for 5 seconds
        sleep(t)

        # Turn off all pixels
        sense.clear()

    if color == "green":
        # Set all pixels to green
        sense.clear((0, 127, 0))

        # Wait for t seconds
        sleep(t)

        # Turn off all pixels
        sense.clear()


def sense_message(msg="a", text_color=(127, 127, 127), bg_color=(0, 0, 0)):
    """
    Display a message on the Sense HAT LED matrix.

    Parameters: msg (str): The message to display. Default is "a".
    text_color (tuple): The RGB color tuple for the text. Default is (127,
    127, 127). bg_color (tuple): The RGB color tuple for the background.
    Default is (0, 0, 0).
    """
    # Set background color
    sense.clear(bg_color)

    # Display the message on the LED matrix
    sense.show_message(
        msg, text_colour=text_color, back_colour=bg_color, scroll_speed=0.05
    )

    # Wait for the scrolling to finish
    while sense.stick.get_events():
        pass
