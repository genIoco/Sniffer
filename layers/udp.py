from layers.layer import Layer
from packet import Packet


class UDP(Layer):
    'UDP帧结构'

    def DecodeFromBytes(self, data: bytes):
        self.srcPort = int.from_bytes(data[0:2], "big")
        self.dstPort = int.from_bytes(data[2:4], "big")
        self.length = int.from_bytes(data[4:6], "big")
        self.checksum = int.from_bytes(data[6:8], "big")
        self.header = data[0:8]
        self.payload = data[8:]

    @property
    def NextLayerType(self):
        # TODO 添加按照端口判断上层协议
        return "UNKNOWN"

    @property
    def Info(self):
        info = "%s → %s " % (self.srcPort, self.dstPort)
        info += "Len=%s " % (len(self.payload)
                             if len(self.payload) > 8 else 0)
        return info

    @property
    def Detail(self):
        return [
            f"User Datagram Protocol, Src Port: {self.srcPort}, Dst Port: {self.dstPort}",
            [
                f"Source Port: {self.srcPort}",
                f"Destination Port: {self.dstPort}",
                f"Length: {len(self.header+self.payload)}",
                f"Checksum: {'0x{:0>4x}'.format(self.checksum)}",
                # UDP追踪流,五元组，类变量，实例变量
                f"[Stream index]: 0",
                f"UDP payload ({len(self.payload)} bytes)",
            ]
        ]


def DecodeUDP(data: bytes, packet: Packet) -> bool:
    udp = UDP()
    udp.DecodeFromBytes(data)
    packet.AddLayer(udp)
    packet.SetTransportLayer(udp)
    packet.NextDecoder(udp.NextLayerType)
    return True
