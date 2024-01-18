import smbus
import time
import sys
import pyqtgraph as pg
import pyqtgraph.exporters

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTranslator, QDateTime
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.uic.properties import QtGui

from termocouple import spi1, read_temp1, cmd, spi0, read_temp
from ui_file.complex_ui import Ui_MainWindow
from localization import *
from camera_control import *
# from termocouple import *


class MainWindow(QMainWindow, Local_Language, Microscope):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_dir = os.getcwd()
        self.ui = Ui_MainWindow()
        self.trans = QTranslator()
        self.ui.setupUi(self)

        self.is_camera1_opened = False

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(20)

        self._timer1 = QtCore.QTimer(self)
        self._timer1.timeout.connect(self.request_reading)
        self._timer1.setInterval(1000)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.comboBox.currentIndexChanged.connect(self.changeLanguage)
        self.ui.leftLiteMenu.setVisible(False)
        self.data = {'x': [], 'y': []}
        self.ui.cameraOn.clicked.connect(self.start_camera)
        self.ui.buttonUp.clicked.connect(self.moveUp)
        self.ui.buttonDown.clicked.connect(self.moveDown)
        self.ui.buttonLeft.clicked.connect(self.moveLeft)
        self.ui.buttonRight.clicked.connect(self.moveRight)
        self.ui.buttonTable_2.clicked.connect(self.request_reading)
        self.ui.buttonSaveGraph.clicked.connect(self.saveGraph)

        # # self.buttonAuto.clicked.connect()
        # self.bus = smbus.SMBus(1)
        # self.SLAVE_ADDRESS = 0x04

    # def start_camera(self):
    #     self.is_camera1_opened = ~self.is_camera1_opened
    #     self.ui.buttonAuto.setChecked(self.is_camera1_opened)
    #     if self.is_camera1_opened:
    #         self._timer.start()
    #         self._queryFrame()
    #     else:
    #         self._timer.stop()

    def saveGraph(self):
        self.exporter = pg.exporters.ImageExporter(self.ui.graphTemp.plotItem)
        self.exporter.params.param('width').setValue(700, blockSignal=self.exporter.widthChanged)
        self.exporter.params.param('height').setValue(500, blockSignal=self.exporter.heightChanged)
        self.clock = (str(time.strftime("%d.%m.%Y  %H:%M:%S", time.localtime())))
        self.exporter.export(f'{self.clock}.png')


    def graph_temp(self, temp3):

        timestamp = QDateTime.currentDateTime().toSecsSinceEpoch()
        self.data['x'].append(timestamp)
        self.data['y'].append(temp3)
        self.graphTemp.plot(pen='y').setData(self.data['x'], self.data['y'])
        self.graphTemp.setXRange(timestamp - 60, timestamp)

    def temp_1(self):
        resp_1 = spi0.xfer2(cmd)
        self.temp1 = read_temp(spi0)  # Чтение температуры с первого датчика

        if resp_1 == [0, 0, 0, 0]:
            # msg = QMessageBox()
            # msg.setWindowTitle("Warning")
            # msg.setText("Warning - Thermocouple №1 NONE")
            # msg.setIcon(QMessageBox.Warning)
            # msg.exec_()
            self.label_13.setPixmap(QtGui.QPixmap(":/whiteIcons/icons-white/red.svg"))
            self.label_12.setText("WARNING")

        else:

            self.label_13.setPixmap(QtGui.QPixmap(":/whiteIcons/icons-white/green.svg"))
            self.label_12.setText(f"Thermocouple №1 - {self.temp1} °C")

    def temp_2(self):
        resp_2 = spi1.xfer2(cmd)
        self.temp2 = read_temp1(spi1)  # Чтение температуры со второго датчика

        if resp_2 == [0, 0, 0, 0]:
            # msg = QMessageBox()
            # msg.setWindowTitle("Warning")
            # msg.setText("Warning - Thermocouple №2 NONE")
            # msg.setIcon(QMessageBox.Warning)
            # msg.exec_()
            self.label_11.setPixmap(QtGui.QPixmap(":/whiteIcons/icons-white/red.svg"))
            self.label_14.setText("WARNING")
        else:

            self.label_11.setPixmap(QtGui.QPixmap(":/whiteIcons/icons-white/green.svg"))
            self.label_14.setText(f"Thermocouple №2 - {self.temp2} °C")

    @QtCore.pyqtSlot()
    def request_reading(self):

        self._timer1.start()

        self.temp_1()
        self.temp_2()

        temp3 = (self.temp1 + self.temp2) // 2
        self.tempLabel.setText(f"{temp3} °C")

        self.graph_temp(temp3)

    def moveUp(self):
        return
        # self.bus.write_byte(self.SLAVE_ADDRESS, ord('u'))

    def moveDown(self):
        return
#         self.bus.write_byte(self.SLAVE_ADDRESS, ord('d'))

    def moveLeft(self):
        return
        # self.bus.write_byte(self.SLAVE_ADDRESS, ord('l'))

    def moveRight(self):
        return
        # self.bus.write_byte(self.SLAVE_ADDRESS, ord('r'))

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.leftMenu.findChildren(QPushButton)

        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def on_buttonHome_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_buttonTable_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_buttonGenerator_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_buttonCameraControl_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_buttonVacuum_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_buttonHistory_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_buttonSettings_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())