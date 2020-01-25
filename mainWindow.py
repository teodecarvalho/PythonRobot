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

        self.ui.ChooseFile.clicked.connect(self.select_file)
        self.ui.ActivatePump.clicked.connect(self.activate_pump)
        self.ui.DeactivatePump.clicked.connect(self.deactivate_pump)
        self.ui.ConnectPump.clicked.connect(self.connect_pump)
        self.ui.DisconnectPump.clicked.connect(self.disconnect_pump)
        self.ui.ConnectRobot.clicked.connect(self.connect_robot)
        self.ui.DisconnectRobot.clicked.connect(self.disconnect_robot)
        # Clique na table de serviços em execução
        #self.ui.tableView_ServExec.selectionModel().selectionChanged.connect(self.listar_itens)

    def select_file(self):
        self.ui.FileName.setText(QFileDialog.getOpenFileName()[0])

    def activate_pump(self):
        self.robot.activate_pump()
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Activated!")

    def deactivate_pump(self):
        self.robot.deactivate_pump()
        QMessageBox.information(QMessageBox(), "Sucess", "Pump Deactivated!")

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

if __name__ == "__main__":
    robot = Robot()
    app = QApplication(sys.argv)  # instantiate a QtGui (holder for the app)
    window = MyApp(robot)
    window.show()
    sys.exit(app.exec_())