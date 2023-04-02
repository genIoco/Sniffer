from layers.enums import EthernetType
from layers.layer import Layer
from packet import Packet
from util.util import GetBits


class Ethernet(Layer):
    '以太网帧类结构'
    name = "ethernet"

    def __init__(self) -> None:
        super().__init__()
        self.srcMAC = ""
        self.dstMAC = ""
        self.ethernetType = 0
        self.length = 0
        self.padding = None

    def DecodeFromBytes(self, data: bytes):
        """以太网数据包解码器"""
        self.dstMAC = data[0:6].hex(':')
        self.srcMAC = data[6:12].hex(':')
        self.ethernetType = GetBits(data[12:14], 0, 16)
        self.length = len(data)
        self.header = data[:14]
        self.payload = data[14:]

    @property
    def NextLayerType(self) -> str:
        return EthernetType(self.ethernetType).name

    @property
    def Info(self):
        return self.NextLayerType

    @property
    def Detail(self):
        return [
            f"Ethernet II, Src: {self.srcMAC}, Dst: {self.dstMAC}",
            [
                f"Destination: {self.dstMAC}",
                f"Source: {self.srcMAC}",
                f"Type: {self.NextLayerType}({'0x{:0>4x}'.format(self.ethernetType).zfill(4)})"
            ]
        ]


def DecodeEthernet(data: bytes, packet: Packet):
    eth = Ethernet()
    eth.DecodeFromBytes(data)
    packet.AddLayer(eth)
    packet.SetLinkLayer(eth)
    packet.NextDecoder(eth.NextLayerType)
