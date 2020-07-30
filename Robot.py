import serial
import time
import re

class Robot:
    def __init__(self):
        self.pump_active = False
        self.hold = False
        self.resume = True

    def connect_pump(self, port):
        self.pump = serial.Serial(port, 9600, timeout=3)
        time.sleep(2)

    def disconnect_pump(self):
        self.pump.close()

    def connect_robot(self, port):
        self.robot = serial.Serial(port, 115200, timeout=3)
        time.sleep(2)
        self.robot.write(b"\r\n\r\n")
        time.sleep(2)  # Wait for grbl to initialize
        self.robot.flushInput()  # Flush startup text in serial input

    def disconnect_robot(self):
        self.robot.close()

    def activate_pump(self):
        self.pump.write(b'<sc>')
        self.pump_active = True
        time.sleep(3)

    def deactivate_pump(self):
        self.pump.write(b'<hc>')
        self.pump_active = False
        time.sleep(1)

    def send_cmd_pump(self, cmd):
        self.pump.flushInput()
        time.sleep(.01)
        print(cmd)
        self.pump.write(cmd.encode())
        #pump_out = self.pump.readline()  # Wait for robot response with carriage return
        #print(pump_out.strip())

    def move_home(self):
        self.send_gcode_str("$H")
        self.send_gcode_str("G90")

    def move_left(self, step_size):
        self.send_gcode_str("G21 G91 G0 X-" + str(step_size))
        self.send_gcode_str("G90")

    def move_right(self, step_size):
        self.send_gcode_str("G21 G91 G0 X" + str(step_size))
        self.send_gcode_str("G90")

    def move_fwd(self, step_size):
        self.send_gcode_str("G21 G91 G0 Y" + str(step_size))
        self.send_gcode_str("G90")

    def move_rev(self, step_size):
        self.send_gcode_str("G21 G91 G0 Y-" + str(step_size))
        self.send_gcode_str("G90")

    def move_up(self, step_size):
        self.send_gcode_str("G21 G91 G0 Z" + str(step_size))
        self.send_gcode_str("G90")

    def move_down(self, step_size):
        self.send_gcode_str("G21 G91 G0 Z-" + str(step_size))
        self.send_gcode_str("G90")

    def activate_pump_if_z_negative(self, l):
        try:
            z = float(re.findall("Z([0-9\\-\\.]+)", l)[0])
        except IndexError:
            return None
        if z < 0 and not self.pump_active:
            self.activate_pump()
        elif z >= 0 and self.pump_active:
            self.deactivate_pump()

    def send_gcode_str(self, gcode_str):
        self.robot.flushInput()
        time.sleep(.01)
        print(gcode_str)
        gcode_str += "\n"
        self.robot.write(gcode_str.encode())
        grbl_out = self.robot.readline()  # Wait for robot response with carriage return
        print(grbl_out.strip())
        return(grbl_out.strip().decode("ascii"))

    def check_if_idle(self):
            try:
                status = self.send_gcode_str("?")
                return "Idle" in status
            except:
                return False

    def send_gcode_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                l = line.strip()
                self.activate_pump_if_z_negative(l)
                print(l)
                self.send_gcode_str(l)
                while not self.check_if_idle():
                    pass

    def write_gcode(self, dlayers, nlayers, burnin, polygon, filename):
        gcode = """
        $H
        G21
        %s """ % (burnin) + polygon * nlayers + \
        """       
        G00 Z%s
        G10 P0 L20 Z0
        """ %(dlayers)  + \
        """
        G00 Z00.000000
        $H
        """
        with open(filename, "w") as file:
            file.write(gcode)


