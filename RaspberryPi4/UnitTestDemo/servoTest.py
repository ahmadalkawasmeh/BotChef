from time import sleep
from gpiozero import Button, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

gpioFac = PiGPIOFactory()

s = Servo(12, pin_factory=gpioFac)
b = Button(16, pin_factory=gpioFac)


# p.ChangeDutyCycle(3)
# sleep(1)
# p.ChangeDutyCycle(12)
# sleep(1)

def activate_servo():
    s.max()
    sleep(1)
    s.min()

while(True):
    if b.is_pressed:
        activate_servo()
    sleep(0.1)

