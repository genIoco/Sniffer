import socket
from layers.enums import ARPType
from layers.layer import Layer
from packet import Packet
from util.util import GetBits, InetNtop


class ARP(Layer):
    'ARP帧结构'

    def __init__(self) -> None:
        super().__init__()
        self.hardware = 0x0001
        self.protocol = 0x0800
        self.op = None
        self.hardwareLenght = 6
        self.protocolLenght = 4
        self.srcMAC = None
        self.srcIP = None
        self.dstMAC = None
        self.dstIP = None

    def DecodeFromBytes(self, data: bytes):
        """ARP帧结构解码器"""
        self.hardware = GetBits(data[:2], 0, 16)
        self.protocol = GetBits(data[2:4], 0, 16)
        self.hardwareLenght = GetBits(data[4], 0, 8)
        self.protocolLenght = GetBits(data[5], 0, 8)
        self.op = GetBits(data[6:8], 0, 16)
        self.srcMAC = data[8:14].hex(':')
        self.srcIP = InetNtop(socket.AF_INET, data[14:18])
        self.dstMAC = data[18:24].hex(':')
        self.dstIP = InetNtop(socket.AF_INET, data[24:28])
        self.header = data[:28]
        self.payload = data[28:]

    @property
    def Info(self):
        info = ""
        if ARPType(self.op).name == 'request':
            info += "Who has %s? Tell %s" % (self.srcIP, self.dstIP)
        elif ARPType(self.op).name == 2:
            info += "%s is at %s" % (self.srcIP, self.srcMAC)
        return info

    @property
    def Detail(self):
        return [
            f"Address Resolution Protocol ({ARPType(self.op).name})",
            [
                # TODOARP具体协议类型
                f"Hardware type: Ethernet (1)",
                f"Protocol type: IPv4 (0x0800)",
                f"Hardware size: {self.hardwareLenght}",
                f"Protocol size: {self.protocolLenght}",
                f"Opcode: request(1)",
                f"Sender MAC address: {self.srcMAC}",
                f"Sender IP address: {self.srcIP}",
                f"Target MAC address: {self.dstMAC}",
                f"Target IP address: {self.dstIP}"
            ]
        ]


def DecodeARP(data: bytes, packet: Packet):
    arp = ARP()
    arp.DecodeFromBytes(data)
    packet.AddLayer(arp)
    packet.NextDecoder(arp.NextLayerType)
