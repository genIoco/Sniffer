from layers.layer import Layer
from packet import Packet


class UDP(Layer):
    'UDP帧结构'
    srcPort = None
    dstPort = None
    length = None
    checksum = None

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
        return super().NextLayerType

def DecodeUDP(data: bytes, packet: Packet) -> bool:
    udp = UDP()
    udp.DecodeFromBytes(data)
    packet.AddLayer(udp)
    packet.SetTransportLayer(udp)
    packet.NextDecoder(udp.NextLayerType)
    return True
