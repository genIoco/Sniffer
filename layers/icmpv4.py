from layers.enums import ICMPv4Type
from layers.layer import Layer
from packet import Packet
from util.util import GetBits


class ICMPv4(Layer):
    "ICMPv4帧结构"

    def __init__(self) -> None:
        super().__init__()
        self.type = None
        self.code = None
        self.checksum = 0
        self.rest = 0

    def DecodeFromBytes(self, data: bytes):
        self.type = GetBits(data[0])
        self.code = GetBits(data[1])
        self.checksum = GetBits(data[2:4], 0, 16)
        self.rest = GetBits(data[4:8], 0, 32)
        self.header = data[:8]
        self.payload = data[8:]

    @property
    def Info(self):
        return f"Echo (ping) {ICMPv4Type(self.type).name} id={'0x{:0>4x}'.format(self.rest>>16)}, seq={self.rest&0xffff}"

    @property
    def Detail(self):
        return [
            f"Internet Control Message Protocol",
            [

                f"Type: {self.type} (Echo (ping) { ICMPv4Type(self.type).name})",
                # TODO icmp以下字段的含义是根据icmp的类型字段决定的,仍需处理
                f"Code: {self.code}",
                f"Checksum: {'0x{:0>4x}'.format(self.checksum)}",
                f"Identifier(LE): {self.rest>>16} ({'0x{:0>4x}'.format(self.rest>>8)})",
                f"Sequence Number(LE): {self.rest&0xffff} ({'0x{:0>4x}'.format(self.rest&0xff)})",
                [
                    f"Data({len(self.payload)} bytes)",
                    [
                        f"Data: {self.payload.hex()}",
                        f"[Length: {len(self.payload)}]"
                    ]
                ]
            ]
        ]


def DecodeICMPv4(data: bytes, packet: Packet):
    icmp = ICMPv4()
    icmp.DecodeFromBytes(data)
    packet.AddLayer(icmp)
    packet.NextDecoder(icmp.NextLayerType)
