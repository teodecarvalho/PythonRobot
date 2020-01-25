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

        # Botão cadastrar novo cliente
        self.ui.ChooseFile.clicked.connect(self.selectFile)
        # Clique na table de serviços em execução
        #self.ui.tableView_ServExec.selectionModel().selectionChanged.connect(self.listar_itens)

    def selectFile(self):
        self.ui.FileName.setText(QFileDialog.getOpenFileName()[0])

    def activate_pump(self):
        self.robot.activate_pump()

    def deactivate_pump(self):
        self.robot.deactivate_pump()

    def deactivate_pump(self):
        self.pump_active = False

    def connect_pump(self):
        pump_port = self.ui.PumpPort.text()


if __name__ == "__main__":
    robot = Robot()
    app = QApplication(sys.argv)  # instantiate a QtGui (holder for the app)
    window = MyApp(robot)
    window.show()
    sys.exit(app.exec_())