from layers.layer import Layer
from packet import Packet
from util.util import *
from layers.enums import IPProtocol


class IPv4(Layer):
    'IPv4帧结构'

    def __init__(self) -> None:
        super().__init__()
        self.name = 'IPv4'
        self.version = 4
        self.hlength = 5
        self.tos = 0
        self.length = None
        self.id = 0
        self.flags = 0
        self.fragoffset = 0
        self.ttl = None
        self.protocol = None
        self.checksum = 0
        self.srcIP = None
        self.dstIP = None
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
        self.dstIP = InetNtop(socket.AF_INET, data[16:20])
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

    @property
    def Info(self):
        return self.NextLayerType + f"({self.protocol})"

    @property
    def Detail(self):
        return [
            f"Internet Protocol Version 4, Src: {self.srcIP}, Dst: {self.dstIP}",
            [

                f"{hex(self.version)[2:].zfill(4)} .... = Version: {self.version}",
                f".... {hex(self.hlength)[2:].zfill(4)} = Header Length: {self.hlength*4} bytes ({self.hlength})",
                # TODO ipv4的TOS字段具体含义解析
                [
                    f"Differentiated Services Field: {'0x{:0>2x}'.format(self.tos)} (DSCP: CS0, ECN: Not-ECT)",
                    [
                        f"{'0x{:0>2x}'.format(self.tos>>4)} {'0x{:0>2x}'.format((self.tos>>2)&0x3)}.. = Differentiated Services Codepoint: Default ({self.tos>>2})",
                        f".... ..{'0x{:0>2x}'.format(self.tos&0x3)} = Explicit Congestion Notification: Not ECN-Capable Transport ({self.tos&0x3})"
                    ]
                ],
                f"Total Length: {self.length}",
                f"Identification: {hex(self.id)} ({self.id})",
                [
                    f"{hex(self.flags)[2:].zfill(3)}. .... = Flags: {hex(self.flags)}, Don't fragment",
                    [
                        f"{self.flags>>2}... .... = Reserved bit: {'S' if self.flags>>2 else 'Not s'}et",
                        f".{self.flags>>1&1}.. .... = Don't fragment: {'S' if self.flags>>1&1 else 'Not s'}et",
                        f"..{self.flags>>2&1}. .... = More fragments: {'S' if self.flags>>2&1 else 'Not s'}et"
                    ]
                ],
                f"...0 0000 0000 0000 = Fragment Offset: 0",
                f"Time to Live: {self.ttl}",
                f"Protocol: {self.NextLayerType} ({self.protocol})",
                f"Header Checksum: {'0x{:0>4x}'.format(self.checksum).zfill(0)}",
                f"Source Address: {self.srcIP}",
                f"Destination Address: {self.dstIP}",
            ],
        ]


def DecodeIPv4(data: bytes, packet: Packet):
    ip = IPv4()
    ip.DecodeFromBytes(data)
    packet.AddLayer(ip)
    packet.SetNetworkLayer(ip)
    packet.NextDecoder(ip.NextLayerType)
