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
        self.pump.write(b'a')
        self.pump_active = True

    def send_cmd_pump(self, cmd):
        self.pump.flushInput()
        time.sleep(.01)
        print(cmd)
        self.pump.write(cmd.encode())
        pump_out = self.pump.readline()  # Wait for robot response with carriage return
        print(pump_out.strip())

    def close_pump(self):
        self.pump.write(b'x')
        self.pump_active = False

    def deactivate_pump(self):
        self.close_pump()

    def start_pump(self):
        self.close_pump()

    def stop_pump(self):
        self.pump.write(b'h')
        self.pump_active = False

    def update_pump_speed(self, pulse):
        cmd_str = "s" + str(pulse)
        self.pump.write(cmd_str.encode())

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

    def resume_activity(self):
        self.resume = True

    def send_hold_signal(self):
        self.hold = True

    def hold_activity(self):
        previous_pump_status = self.pump_active
        if self.pump_active:
            self.deactivate_pump()
        while not self.resume:
            pass
        self.resume = False
        self.hold = False
        if previous_pump_status:
            self.activate_pump()

    def activate_pump_if_z_negative(self, l):
        try:
            z = float(re.findall("Z([0-9\\-\\.]+)", l)[0])
        except IndexError:
            return None
        if z < 0 and not self.pump_active:
            self.activate_pump()
        elif z > 0 and self.pump_active:
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

    def reset_zero(self):
        self.send_gcode_str("G10 P0 L20 X0 Y0 Z0")

    def return_to_zero(self):
        self.send_gcode_str("G90 G0 Z1.0")
        self.send_gcode_str("G90 G0 X0 Y0 Z0")

    def send_gcode_file(self, file_path):
        self.deactivate_pump()
        with open(file_path, 'r') as file:
            for line in file:
                # if self.robot.hold:
                #    self.robot.hold_activity()
                l = line.strip()
                self.activate_pump_if_z_negative(l)
                print(l)
                self.send_gcode_str(l)
                while not self.check_if_idle():
                    pass
            self.return_to_zero()

    def write_gcode(self, nlayers, burnin, polygon, filename):
        gcode = """
        G21

        G01 Z-0.050000 F300.0(Penetrate)
        %s """ % (burnin) + """
        %s
        G00 Z0.500000
        G10 P0 L20 Z0
        """ % (polygon) * nlayers + """
        G00 Z2.000000
        G00 X0.0000 Y0.0000
        """
        with open(filename, "w") as file:
            file.write(gcode)


