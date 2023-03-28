from layers.layer import Layer
from packet import Packet
from util.util import *
from layers.enums import IPProtocol

# TODO 标记字段是否需要解析到帧结构中
URG = 0x20
ACK = 0x10
PSH = 0x08
RST = 0x04
SYN = 0x02
FIN = 0x01


class IPv4(Layer):
    'IPv4帧结构'

    def __init__(self) -> None:
        super().__init__()
        self.name = 'IPv4'
        self.version = 4
        self.hlength = 5
        self.tos = None
        self.length = None
        self.id = None
        self.flags = None
        self.fragoffset = None
        self.ttl = None
        self.protocol = None
        self.checksum = None
        self.srcIP = None
        self.dsrIP = None
        self.options = None

    # IP数据包解码器
    def DecodeFromBytes(self, data: bytes):
        self.version = GetBits(data[0], 0, 4)
        self.hlength = GetBits(data[0], 4, 4)
        self.tos = GetBits(data[1], 0, 8)
        self.length = GetBits(data[2:4], 0, 16)
        self.id = GetBits(data[4:6], 0, 16)
        self.flags = GetBits(data[6], 0, 3)
        self.fragoffset = GetBits(data[6:8], 3, 13)
        self.ttl = GetBits(data[8], 0, 8)
        self.protocol = data[9]
        self.checksum = GetBits(data[10:12], 0, 16)
        self.srcIP = InetNtop(socket.AF_INET, data[12:16])
        self.dsrIP = InetNtop(socket.AF_INET, data[16:20])
        hLen = 4 * int(self.hlength)
        if (hLen - 20) > 0:
            self.options = data[20:hLen]
        self.header = data[:hLen]
        self.payload = data[hLen:]

    # 获取IP下一层类型
    # TODO IP层可能会分片，下一层类型需要重新定义一类分片类型
    @property
    def NextLayerType(self):
        return IPProtocol(self.protocol).name


def DecodeIPv4(data: bytes, packet: Packet):
    ip = IPv4()
    ip.DecodeFromBytes(data)
    packet.AddLayer(ip)
    packet.SetNetworkLayer(ip)
    packet.NextDecoder(ip.NextLayerType)
