import serial
import time
import re

# Open grbl serial port
s = serial.Serial('COM4', 115200, timeout=3)
s_pump = serial.Serial('COM6', 9600, timeout=3)
time.sleep(2)   # Wait arduino to reset

def send_gcode_str(gcode_str, serial):
    serial.flushInput()
    time.sleep(.01)
    gcode_str += "\n"
    serial.write(gcode_str.encode())
    grbl_out = serial.readline()  # Wait for grbl response with carriage return
    print(grbl_out.strip())
    return(grbl_out.strip().decode("ascii"))

# Wake up grbl
s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

# with open("gcode_configurations", "r") as gcode_config:
#     for line in gcode_config.readlines():
#         gcode_cmd = line.split(" ")[0]
#         s.write(gcode_cmd.encode())
#         grbl_out = s.readline()  # Wait for grbl response with carriage return
#         print(grbl_out.strip())

def get_z(line):
    global pump_active
    s_pump.flushInput()  # Flush text in serial input
    try:
        z = float(re.findall("Z([0-9\\-\\.]+)", line)[0])
        if z < 0 and not pump_active:
            pump_active = True
            while s_pump.readline().decode('ascii').rstrip("\r\n") != 'Activate pump signal received':
                s_pump.flushInput()
                s_pump.write(b'a')
        elif z >= 0 and pump_active:
            pump_active = False
            while s_pump.readline().decode('ascii').rstrip("\r\n") != 'Deactivate pump signal received':
                s_pump.flushInput()
                s_pump.write(b'd')
    except IndexError:
        print("IndexError")
        print(l)
    return None

# Set initial position
send_gcode_str("G10 P0 L20 X0 Y0 Z0", s)

# Stream g-code to grbl
# Open g-code file
f = open('./gcode_files/output_0015.ngc', 'r');
pump_active = False
for line in f:
    l = line.strip() # Strip all EOL characters for consistency
    get_z(l)
    print('Sending: ' + l)
    cmd_gcode = l
    send_gcode_str(cmd_gcode, s) # Send g-code block to grbl
    # remain = True
    # while remain:
    #     grbl_out = s.readline()  # Wait for grbl response with carriage return
    #     print(grbl_out.strip())
    #     remain = input("Continuar?")
    while True:
        try:
            status = send_gcode_str("?", s)
            if "Idle" in status:
                break
        except:
            pass

send_gcode_str("G90 G0 X0 Y0 Z0", s)
# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
f.close()
s.close()
s_pump.close()