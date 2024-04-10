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
    
def set_angle(angle):
    mapped_angle = (angle / 180) * 2 - 1
    s.value = mapped_angle
    sleep(0.5)
    
set_angle(160)

while(True):
    if b.is_pressed:
        set_angle(50)
        set_angle(160)
    sleep(0.1)

