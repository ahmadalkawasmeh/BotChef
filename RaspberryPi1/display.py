import RPi.GPIO as GPIO
from RPLCD import CharLCD

def initialize_lcd():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 21], numbering_mode=GPIO.BCM)
	return lcd


def display_message(lcd, message):
    lcd.clear()
    lcd.write_string(message)
    global msg
    msg = message

    
    
   
def get_message(lcd):
    global msg
    return msg




