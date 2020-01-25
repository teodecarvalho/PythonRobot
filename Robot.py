import serial
import time
import re

class Robot:
    def __init__(self):
        pass

    def connect_pump(self, port):
        self.pump = serial.Serial(port, 9600, timeout=3)

    def disconnect_pump(self):
        self.pump.close()

    def connect_robot(self, port):
        self.robot = serial.Serial(port, 115200, timeout=3)

    def disconnect_robot(self):
        self.robot.close()

    def activate_pump(self):
        self.pump.write(b'a')

    def deactivate_pump(self):
        self.pump.write(b'd')
