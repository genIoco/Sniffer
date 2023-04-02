from packet import Packet
from layers.layer import Layer


class Unknown(Layer):
    '未识别数据帧类型'
    name = 'unknown'

    def __init__(self) -> None:
        super().__init__()

    def DecodeFromBytes(self, data: bytes):
        return super().DecodeFromBytes(data)

    @property
    def Info(self):
        return "未知帧格式"

    @property
    def Detail(self):
        return [
            f"Data ({len(self.header)} bytes)",
            [
                f"Data: {self.header.hex()}",
                f"[Length: {len(self.header)}]"
            ]
        ]


def DecodeUnknown(data: bytes, packet: Packet):
    unknown = Unknown()
    unknown.DecodeFromBytes(data)
    packet.AddLayer(unknown)
