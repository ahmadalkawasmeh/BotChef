### Course: SYSC 3010
### Project Title: BotChef
### Group: L2-G12
### Group Members: Abdal Alkawasmeh | Ahmad Alkawasmeh | Ryan Rizk | Zach Gregory
### TA: Ben Earle

---

**Project Summary**

The project aimed to develop an automated sandwich maker system utilizing Python and multiple Raspberry Pi microprocessors. Key technologies involved include:

* TCP and HTTP messages for internode communication
* Firebase real-time database for data synchronization across the system
* SPI and I2C protocols for sensor and actuator interfacing
* Flask and HTML for GUI implementation
* Twilio API for text message notifications
* Ultrasonic sensors, infrared proximity sensor, LCD display, servo motors, and stepper motors

**Repository Structure Description**

The repository is structured into subdirectories, each representing a node in the system. Each node, consisting of a Raspberry Pi, is responsible for a subsystem with specific functionality. The subdirectories contain:

* Unit test scripts ensuring proper operation of each module
* RaspberryPi1: "GUI Pi" responsible for web-based Graphical User Interface
* RaspberryPi2: "Conveyor Belt Pi" responsible for conveyor belt movement and bread dispensing
* RaspberryPi3: "Sauce Pi" responsible for sauce dispensing mechanism
* RaspberryPi4: "Toppings Pi" responsible for toppings dispensing mechanism

**Installation Instructions**

To install and run the system:

1. Clone the project and save each subdirectory on the respective Raspberry Pi.
2. Execute app.py on RaspberryPi1.
3. Execute main_pi2.py on RaspberryPi2.
4. Execute main_pi3.py on RaspberryPi3.
5. Execute main_pi4.py on RaspberryPi4.
6. Place an order through the web GUI running on RaspberryPi1.

The system will then operate as follows:

* The first slice of bread will be dispensed, moving onto the assembly station.
* The assembly station will dispense toppings and sauce.
* Lastly, the sandwich will be moved back to the first station for the second slice of bread dispensing.

While the system runs, monitor the terminal of each subsystem to observe messages passing between nodes. Lack of messages indicates a communication error. Additionally, ensure all unit tests in each subsystem pass successfully (see Docstring of functions that fail to pass the test, if any, for more information).
