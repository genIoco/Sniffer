from layers.layer import Layer
from packet import Packet
from util.util import GetBits

_FLAGS = {
    'URG': 1 << 6,
    'ACK': 1 << 5,
    'PSH': 1 << 4,
    'RST': 1 << 3,
    'SYN': 1 << 2,
    'FIN': 1
}


class TCP(Layer):
    "TCP帧结构"
    def __init__(self) -> None:
        super().__init__()
        self.srcPort = None
        self.dstPort = None
        self.seq = None
        self.ack = None
        self.hlength = 5
        self.reserved = None
        self.flags = 0
        self.windowSize = None
        self.checksum = None
        self.urgent = None
        self.options = None
        self.padding = None

    # TODO tcp的options选项似乎也有部分内容需要处理
    def DecodeFromBytes(self, data: bytes):
        """TCP数据包解码器"""
        self.srcPort = GetBits(data[0:2], 0, 16)
        self.dstPort = GetBits(data[2:4], 0, 16)
        self.seq = GetBits(data[4:8], 0, 32)
        self.ack = GetBits(data[8:12], 0, 32)
        self.hlength = GetBits(data[12], 0, 4)
        self.reserved = GetBits(data[12:14], 4, 6)
        self.flags = GetBits(data[12:14], 10, 6)
        self.windowSize = GetBits(data[14:16], 0, 16)
        self.checksum = GetBits(data[16:18], 0, 16)
        # TODO 紧急指针也要处理
        self.urgent = GetBits(data[18:20], 0, 16)
        hLen = 4 * self.hlength
        if (hLen - 20) > 0:
            self.options = data[21:hLen]

        self.header = data[:hLen]
        self.payload = data[hLen:]
    # XXX 根据端口号判断下一层协议类型，但是似乎可能会存在问题
    # TODO上层协议的处理可能会很麻烦

    @property
    def NextLayerType(self):
        return "UNKNOWN"

def DecodeTCP(data: bytes, packet: Packet):
    tcp = TCP()
    tcp.DecodeFromBytes(data)
    packet.AddLayer(tcp)
    packet.SetTransportLayer(tcp)
    packet.NextDecoder(tcp.NextLayerType)
