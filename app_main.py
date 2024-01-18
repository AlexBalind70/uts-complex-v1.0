from login_main import LoginWindow
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)
    windows = LoginWindow()
    windows.show()
    sys.exit(app.exec_())





