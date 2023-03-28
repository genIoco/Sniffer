# -*- coding: UTF-8 -*-
from PySide6.QtWidgets import QApplication, QMainWindow
from scapy.all import *
from decode import NewPacket
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
    app.exec()


class Ifaces:
    '网卡基本信息类'

    def __init__(self) -> None:
        self.ifaces = conf.ifaces.data
        # self.ifaces = get_windows_if_list()

    # 打印网卡信息
    def ShowIfaces(self):
        for iface_name in self.ifaces:
            iface = self.ifaces[iface_name]
            print("name: ", iface.name)
            print("description: ", iface.description)
            print("index: ", iface.index)
            print("mac: ", iface.mac)
            for ip in iface.ips[4]:
                print("IPv4: ", ip)
            for ip in iface.ips[6]:
                print("IPv6: ", ip)


def callback(packet):
    packet.show()


class Sniffer:
    '嗅探类'
    def __init__(self, iface) -> None:
        self.iface = iface
        self.packets = []

    # 模拟抓包
    def Sniff(self):
        # sniff(iface=self.iface, count=2, prn=callback)
        for x in rdpcap('./test.pcapng'):  # type: ignore
            self.packets.append(NewPacket(x.original, "Ethernet"))


if __name__ == "__main__":
    # Ui()
    # ifaces = Ifaces()
    # ifaces.ShowIfaces()
    sniffer = Sniffer("VMware Virtual Ethernet Adapter for VMnet1")
    sniffer.Sniff()
