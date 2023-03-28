import socket
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


def DecodeARP(data: bytes, packet: Packet):
    arp = ARP()
    arp.DecodeFromBytes(data)
    packet.AddLayer(arp)
    packet.NextDecoder(arp.NextLayerType)
