# -*- coding: UTF-8 -*-
from PySide6.QtWidgets import QApplication, QMainWindow
from scapy.all import *
import Ui_ui as mainWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    window.show()
    app.exec()
