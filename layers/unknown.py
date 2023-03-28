from packet import Packet
from layers.layer import Layer


class Unknown(Layer):
    '未识别数据帧类型'

    def __init__(self) -> None:
        super().__init__()

    def DecodeFromBytes(self, data: bytes):
        return super().DecodeFromBytes(data)

def DecodeUnknown(data: bytes, packet: Packet):
    unknown = Unknown()
    unknown.DecodeFromBytes(data)
    packet.AddLayer(unknown)
