# -*- coding: UTF-8 -*-
from PySide2.QtWidgets import QApplication, QMainWindow
from scapy.all import *
import ui.Ui_ui as mainWindow


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


def Ui():
    app = QApplication([])
    window = MainWindow()

    window.show()
    app.exec_()

if __name__ == "__main__":
    Ui()
