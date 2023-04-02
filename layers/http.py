from layers.layer import Layer
from packet import Packet
from util.util import *


class HTTP(Layer):
    'HTTP数据帧结构'
    name = 'http'

    def __init__(self) -> None:
        super().__init__()

    @property
    def Info(self):
        return self.header.decode().splitlines()[0]

    @property
    def Detail(self):
        return [
            f"Hypertext Transfer Protocol",
            self.header.decode().splitlines()
        ]


def DecodeHTTP(data: bytes, packet: Packet):
    http = HTTP()
    http.DecodeFromBytes(data)
    packet.AddLayer(http)
    packet.SetApplicationLayer(http)
