import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

from Robot import Robot

# Main window
Ui_MainWindow, MainWindowBaseClass = uic.loadUiType("MainWindow.ui")

class MyApp(MainWindowBaseClass, Ui_MainWindow):  # gui class
    def __init__(self, robot):
        # The following sets up the gui via Qt
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.robot = robot
        self.ui.PumpPort.setText("COM6")
        self.ui.RobotPort.setText("COM4")

        self.ui.Exit.clicked.connect(self.close)
        self.ui.ChooseFile.clicked.connect(self.select_file)
        self.ui.ActivatePump.clicked.connect(self.activate_pump)
        self.ui.DeactivatePump.clicked.connect(self.deactivate_pump)
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
        self.ui.Hold.clicked.connect(self.robot.send_hold_signal)
        self.ui.Resume.clicked.connect(self.robot.resume_activity)
        self.ui.ResetZero.clicked.connect(self.robot.reset_zero)
        self.ui.SendFile.clicked.connect(self.send_gcode_file)

        self.ui.PumpDelay.valueChanged.connect(self.update_pump_speed)

    def send_gcode_file(self):
        file_path = self.ui.FileName.text()
        self.robot.send_gcode_file(file_path)

    def select_file(self):
        self.ui.FileName.setText(QFileDialog.getOpenFileName()[0])

    def activate_pump(self):
        self.robot.activate_pump()
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Activated!")

    def deactivate_pump(self):
        self.robot.deactivate_pump()
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Deactivated!")

    def update_pump_speed(self):
        pulse = self.ui.PumpDelay.value()
        self.robot.update_pump_speed(pulse)

    def connect_pump(self):
        pump_port = self.ui.PumpPort.text()
        self.robot.connect_pump(pump_port)
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Connected!")

    def disconnect_pump(self):
        self.robot.disconnect_pump()
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Disconnected!")

    def connect_robot(self):
        robot_port = self.ui.RobotPort.text()
        self.robot.connect_robot(robot_port)
        QMessageBox.information(QMessageBox(), "Sucess", "Robot Connected!")

    def disconnect_robot(self):
        self.robot.disconnect_robot()
        QMessageBox.information(QMessageBox(), "Sucess", "Robot Disconnected!")

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