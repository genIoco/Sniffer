# -*- coding: UTF-8 -*-
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTreeWidgetItem, QTreeWidget
from PySide6.QtCore import QObject, Signal
from myscapy import Ifaces, Sniffer
import ui.Ui_ui as mainWindow


class SignalStore(QObject):
    packetSignal = Signal()


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.packets = []
        self.signal = SignalStore()
        self.ifaces = Ifaces()
        self.sniffer = Sniffer(self.packets, self.signal)
        self.showPackets = self.ShowPackets()

        self.Connect()

    def __del__(self):
        pass

    def Connect(self):
        # self.ui.start.clicked.connect(self.StartInface)
        # self.ui.stop.clicked.connect(self.StopInface)
        # self.ui.filter.returnPressed.connect(self.SetFilter)
        # self.ui.info.itemClicked.connect(self.Showdetail)
        # self.ui.raw.cursorPositionChanged.connect.(self.AutoScroll)
        self.ui.string.verticalScrollBar().valueChanged.connect(
            self.ui.raw.verticalScrollBar().setValue)
        self.ui.string.verticalScrollBar().valueChanged.connect(
            self.ui.nums.verticalScrollBar().setValue)
        self.ui.raw.verticalScrollBar().valueChanged.connect(
            self.ui.string.verticalScrollBar().setValue)

        self.signal.packetSignal.connect(lambda: next(self.showPackets))

        self.ShowIfaces()

    def UpdateLineNums(self):
        lineCount = len(self.ui.string.toPlainText()) // 16

        lineNums = "\n".join(
            map(lambda x: hex(x)[2:].zfill(4), range(0, lineCount+1)))
        self.ui.nums.setPlainText(lineNums)

    def StartInface(self):
        self.sniffer.SetIface(self.ui.ifaces.currentData())

        # self.sniffer.Run()
        self.sniffer.LoadFile("./icmp.pcapng")
        self.ui.start.setDisabled(True)
        self.ui.stop.setDisabled(False)

    def StopInface(self):
        self.ui.start.setDisabled(False)
        self.ui.stop.setDisabled(True)
        self.sniffer.Stop()

    def SetFilter(self):
        filter_rule = {
            'protocol': '',
            'ip': '',
            'port': '0'
        }
        filter = self.ui.filter.text()
        # TODO目前仅支持单条命令过滤
        tmp = filter.split('==')
        if len(tmp) != 1:
            filter_rule[tmp[0].strip()] = tmp[1].strip()
        else:
            filter_rule['protocol'] = tmp[0].strip()
        for row in range(len(self.packets)):
            if tmp[0] == '':
                self.ui.info.setRowHidden(row, False)
                continue
            else:
                self.ui.info.setRowHidden(row, True)
            packet = self.packets[row]
            for layer in packet.layers:
                if filter_rule['protocol'] == layer.name:
                    self.ui.info.setRowHidden(row, False)
                    break
            if packet.network is not None and (filter_rule['ip'] == packet.network.srcIP or filter_rule['ip'] == packet.network.dstIP):
                self.ui.info.setRowHidden(row, False)
                continue

            if packet.transport is not None and (int(filter_rule['port']) == packet.transport.srcPort or int(filter_rule['port']) == packet.transport.dstPort):
                self.ui.info.setRowHidden(row, False)
                continue

    def ShowIfaces(self):
        self.ifaces.GetIfaces()
        # self.ui.ifaces.addItems([x.description for x in self.ifaces.devices])
        for x in self.ifaces.devices:
            self.ui.ifaces.addItem(x.description, x.network_name)

    def ShowPackets(self):
        if len(self.sniffer.packets) == 0:
            yield
        for item in self.sniffer.packets:
            row = self.ui.info.rowCount()
            self.ui.info.insertRow(row)
            for col, text in enumerate(item.GetInfo().values()):
                self.ui.info.setItem(row, col, QTableWidgetItem(str(text)))
            self.ui.info.resizeColumnsToContents()
            self.ui.info.scrollToBottom()
            self.ui.info.horizontalHeader().setStretchLastSection(True)
            yield

    def Showdetail(self):
        row = self.ui.info.currentRow()
        packet = self.packets[row]
        self.ui.raw.setText(packet.Dump())
        self.ui.string.setText(packet.String())

        def Make(parent: 'QTreeWidgetItem|QTreeWidget', data: 'list|str') -> QTreeWidgetItem:
            if isinstance(data, str):
                return QTreeWidgetItem(parent, [data, 'data'])
            root = QTreeWidgetItem(parent, [data[0], 'data'])
            children = []
            for item in data[1]:
                child = Make(root, item)
                children.append(child)
            root.addChildren(children)
            return root

        self.ui.detail.clear()
        for data in packet.GetDetail():
            self.ui.detail.addTopLevelItem(Make(self.ui.detail, data))


def Ui():
    app = QApplication([])
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Ui()
