from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import  QMessageBox
from ui_file.login import Ui_Form
from complex_main import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._startPos = None
        self._endPos = None
        self._tracking = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.loginButton.clicked.connect(self.loginBtn_clicked)
## Make the window movable after hide window frame ///////////////////////////
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._tracking:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._startPos = QPoint(a0.x(), a0.y())
            self._tracking = True

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

        ## ============================================================================

    def loginBtn_clicked(self):
        """
        function for login app
        """
        username = self.ui.lineUser.text().strip()
        password = self.ui.linePsw.text().strip()

        # Check the password
        # if password == "0" and username == "admin":
            # Create a new instance of the main window
        self.main_window = MainWindow()
        # Show the new window
        self.main_window.show()
        # Close the login window
        self.close()
        # else:
        #     # Show an error message
        #     QMessageBox.warning(self, "Error", "Incorrect password!")

