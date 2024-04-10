from gpiozero import DistanceSensor
from sense_hat import SenseHat

ultrasonic = DistanceSensor(echo = 20, trigger = 18, threshold_distance = 0.3, max_distance = 2)
sense = SenseHat()

while True:
    if(ultrasonic.distance < ultrasonic.threshold_distance):
        sense.clear(0, 255, 0)
    if(ultrasonic.distance >= ultrasonic.threshold_distance):
        sense.clear(255, 0, 0)
    print(ultrasonic.distance) 
