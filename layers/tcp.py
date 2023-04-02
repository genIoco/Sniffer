from layers.layer import Layer
from packet import Packet
from util.util import GetBits

_FLAGS = {
    'FIN': 1,
    'SYN': 1 << 1,
    'RST': 1 << 2,
    'PSH': 1 << 3,
    'ACK': 1 << 4,
    'URG': 1 << 5,
}


class TCP(Layer):
    "TCP帧结构"

    def __init__(self) -> None:
        super().__init__()
        self.srcPort = None
        self.dstPort = None
        self.rom_seq = 0
        self.seq = 0
        self.rom_ack = 0
        self.ack = 0
        self.hlength = 5
        self.reserved = None
        self.flags = 0
        self.windowSize = None
        self.checksum = 0
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

    @property
    def Info(self):
        # TODO TCP流的判断需要使用五元组进行判断，并且sep的起始标号也需要TCP流来判断
        # 五元组：源IP地址，源端口，目的IP地址，目的端口，和传输层协议
        info = "%s → %s " % (self.srcPort, self.dstPort)
        tmp = []
        for k, v in _FLAGS.items():
            if self.flags & v:
                tmp.append(k)
        info += str(tmp).replace('\'', '')
        info += " Seq=%s " % self.seq
        if 'ACK' in tmp:
            info += "Ack=%s " % self.ack
        info += "Win=%s " % self.windowSize
        info += "Len=%s " % (len(self.payload)
                             if len(self.payload) > 8 else 0)
        return info

    @property
    def Detail(self):
        return [
            f"Transmission Control Protocol, Src Port: {self.srcPort}, Dst Port: {self.dstPort}, Seq: {self.seq}, Len: {len(self.payload)if len(self.payload) > 8 else 0}",
            [
                f"Source Port: {self.srcPort}",
                f"Destination Port: {self.dstPort}",
                f"[Stream index: 0]",
                f"Sequence Number: {self.seq-self.rom_seq}    (relative sequence number)",
                f"Sequence Number(raw): {self.rom_seq}",
                f"[Next Sequence Number: {self.seq-self.rom_seq+1}    (relative sequence number)]",
                f"Acknowledgment Number: {self.ack-self.rom_ack}",
                f"Acknowledgment number(raw): {self.ack}",
                f"{hex(self.hlength)[2:].zfill(4)} ....= Header Length: {4*self.hlength} bytes ({self.hlength})",
                f"Flags: 0x002 (SYN)",
                f"Window: {self.windowSize}",
                f"[Calculated window size: {self.windowSize}]",
                f"Checksum: {'0x{:0>4x}'.format(self.checksum)}",
                f"Urgent Pointer: {self.urgent}",
                f"Options: ({len(self.options)} bytes)" if self.options is not None else "No options"
            ]
        ]


def DecodeTCP(data: bytes, packet: Packet):
    tcp = TCP()
    tcp.DecodeFromBytes(data)
    packet.AddLayer(tcp)
    packet.SetTransportLayer(tcp)
    packet.NextDecoder(tcp.NextLayerType)
