from sense_hat import SenseHat
from time import sleep

# Initialize the Sense HAT
sense = SenseHat()


# Set the LEDs to red or green for t seconds
def sense_led(color, t=5):
    if color == "red":
        # Set all pixels to red
        sense.clear((255, 0, 0))

        # Wait for 5 seconds
        sleep(t)

        # Turn off all pixels
        sense.clear()

    if color == "green":
        # Set all pixels to green
        sense.clear((0, 255, 0))

        # Wait for t seconds
        sleep(t)

        # Turn off all pixels
        sense.clear()


def sense_message(msg="a", text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    # Set background color
    sense.clear(bg_color)

    # Display the message on the LED matrix
    sense.show_message(msg, text_colour=text_color, back_colour=bg_color, scroll_speed=0.05)

    # Wait for the scrolling to finish
    while sense.stick.get_events():
        pass