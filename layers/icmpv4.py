from layers.layer import Layer
from packet import Packet
from util.util import GetBits


class ICMPv4(Layer):
    "ICMPv4帧结构"

    def __init__(self) -> None:
        super().__init__()
        self.type = None
        self.code = None
        self.checksum = None
        self.rest = None

    def DecodeFromBytes(self, data: bytes):
        self.type = GetBits(data[0])
        self.code = GetBits(data[1])
        self.checksum = GetBits(data[2:4], 0, 16)
        self.rest = GetBits(data[4:8],0,32)
        self.header = data[:8]
        self.payload = data[8:]


def DecodeICMPv4(data: bytes, packet: Packet):
    icmp = ICMPv4()
    icmp.DecodeFromBytes(data)
    packet.AddLayer(icmp)
    packet.NextDecoder(icmp.NextLayerType)
