import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from Robot import Robot
import os

# Main window
Ui_MainWindow, MainWindowBaseClass = uic.loadUiType("MainWindow.ui")

class Thread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)
    def run(self):
        self.robot.send_gcode_file(self.file_path)

class MyApp(MainWindowBaseClass, Ui_MainWindow):  # gui class
    def __init__(self, robot):
        # The following sets up the gui via Qt
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fill_file_field()

        self.thread = Thread()

        self.robot = robot
        self.thread.robot = robot

        self.ui.PumpPort.setText("/dev/tty.usbserial-1460")
        self.ui.RobotPort.setText("/dev/tty.usbserial-14140")

        self.connect_robot()
        self.connect_pump()

        self.robot.move_home()

        self.ui.StartPump.clicked.connect(self.activate_pump)
        self.ui.StopPump.clicked.connect(self.deactivate_pump)
        self.ui.WriteGCode.clicked.connect(self.write_gcode)
        self.ui.Exit.clicked.connect(self.stop)
        self.ui.ChooseFile.clicked.connect(self.select_file)
        self.ui.SendCmdPump.clicked.connect(self.send_cmd_pump)
        self.ui.ConnectPump.clicked.connect(self.connect_pump)
        self.ui.DisconnectPump.clicked.connect(self.disconnect_pump)
        self.ui.ConnectRobot.clicked.connect(self.connect_robot)
        self.ui.DisconnectRobot.clicked.connect(self.disconnect_robot)
        self.ui.Left.clicked.connect(self.move_left)
        self.ui.Right.clicked.connect(self.move_right)
        self.ui.Fwd.clicked.connect(self.move_fwd)
        self.ui.Rev.clicked.connect(self.move_rev)
        self.ui.Up.clicked.connect(self.move_up)
        self.ui.Down.clicked.connect(self.move_down)
        self.ui.SendFile.clicked.connect(self.send_gcode_file)
        self.ui.SendCmdRobot.clicked.connect(self.send_cmd_gcode)
        #self.ui.PumpDelay.valueChanged.connect(self.update_pump_speed)

    def write_gcode(self):
        filename = self.ui.FileNameToWrite.text()
        nlayers = int(self.ui.NLayers.text())
        dlayers = self.ui.DLayers.text()
        burnin = self.ui.Burnin.toPlainText()
        polygon = self.ui.Polygon.toPlainText()
        self.robot.write_gcode(dlayers, nlayers, burnin, polygon, filename)
        QMessageBox.information(QMessageBox(), "Sucess", "GCode Written!")

    def send_cmd_gcode(self):
        cmd = self.ui.CmdRobot.text()
        self.robot.send_gcode_str(cmd)

    def send_cmd_pump(self):
        cmd = self.ui.CmdPump.text()
        self.robot.send_cmd_pump(cmd)

    def stop(self):
        self.thread.terminate()
        self.close()

    def fill_file_field(self):
        last_file = os.listdir("./gcode_files")[-1]
        file = "./gcode_files/" + last_file
        self.ui.FileName.setText(file)

    def send_gcode_file(self):
        self.thread.file_path = self.ui.FileName.text()
        #self.update_pump_speed()
        self.thread.start()

    def select_file(self):
        self.ui.FileName.setText(QFileDialog.getOpenFileName()[0])

    def activate_pump(self):
        self.robot.activate_pump()
#        self.update_pump_speed()

    def deactivate_pump(self):
        self.robot.deactivate_pump()
 #       self.update_pump_speed()


#    def update_pump_speed(self):
#        pulse = self.ui.PumpDelay.value()
#        self.robot.update_pump_speed(pulse)

    def connect_pump(self):
        pump_port = self.ui.PumpPort.text()
        self.robot.connect_pump(pump_port)

    def disconnect_pump(self):
        self.robot.disconnect_pump()

    def connect_robot(self):
        robot_port = self.ui.RobotPort.text()
        self.robot.connect_robot(robot_port)

    def disconnect_robot(self):
        self.robot.disconnect_robot()

    def move_home(self):
        self.robot.move_home()

    def move_left(self):
        step_size = self.ui.XYStepSize.value()
        self.robot.move_left(step_size)

    def move_right(self):
        step_size = self.ui.XYStepSize.value()
        self.robot.move_right(step_size)

    def move_fwd(self):
        step_size = self.ui.XYStepSize.value()
        self.robot.move_fwd(step_size)

    def move_rev(self):
        step_size = self.ui.XYStepSize.value()
        self.robot.move_rev(step_size)

    def move_up(self):
        step_size = self.ui.ZStepSize.value()
        self.robot.move_up(step_size)

    def move_down(self):
        step_size = self.ui.ZStepSize.value()
        self.robot.move_down(step_size)

if __name__ == "__main__":
    robot = Robot()
    app = QApplication(sys.argv)  # instantiate a QtGui (holder for the app)
    window = MyApp(robot)
    window.show()
    sys.exit(app.exec_())