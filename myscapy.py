import socket
from util.util import InetNtop
from winpcap import WinPcapDevices, WinPcap
from decode import NewPacket
from scapy.all import rdpcap
import multitasking


class Ifaces:
    '网卡基本信息类'
    class NetworkInterface():
        def __init__(self) -> None:
            self.name = ""
            self.description = ""
            self.network_name = ""
            self.mac = ""
            self.ip4 = []
            self.ip6 = []

    def __init__(self) -> None:
        self.devices = []

    # 打印网卡信息
    def GetIfaces(self):
        with WinPcapDevices() as devices:
            for dev in devices:
                iface = self.NetworkInterface()
                iface.network_name = dev.name.decode()
                iface.description = dev.description.decode()
                addr = dev.addresses
                while addr:
                    if addr[0].addr[0].sa_family == 2:
                        iface.ip4.append(InetNtop(
                            socket.AF_INET, addr[0].addr[0].ipv4_addr))
                    else:
                        iface.ip6.append(InetNtop(
                            socket.AF_INET6, addr[0].addr[0].ipv6_addr))
                    addr = addr[0].next
                self.devices.append(iface)


class Sniffer:
    '嗅探类'

    def __init__(self, packet, signal) -> None:
        self._iface = ""
        self.packets = packet
        self.signal = signal

    def Callback(self, winpcap, param, header, pkt_data):
        packet = NewPacket(pkt_data, "Ethernet", header)
        self.packets.append(packet)
        self.signal.packetSignal.emit()

    def SetIface(self, iface):
        self._iface = iface

    # 网卡抓包
    @ multitasking.task
    def Run(self):
        with WinPcap(self._iface) as capture:
            self._capture = capture
            capture.run(callback=self.Callback, limit=0)

    def Stop(self):
        self._capture.stop()

    @ multitasking.task
    def LoadFile(self, file):
        # XXXlibpacp应该也有读取文件的接口
        for x in rdpcap(file):  # type: ignore
            item = NewPacket(x.original, "Ethernet")
            self.packets.append(item)
            self.signal.packetSignal.emit()


if __name__ == "__main__":
    ifaces = Ifaces()
    ifaces.GetIfaces()
