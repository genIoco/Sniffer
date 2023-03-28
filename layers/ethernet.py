from layers.enums import EthernetType
from layers.layer import Layer
from packet import Packet
from util.util import GetBits


class Ethernet(Layer):
    '以太网帧类结构'
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ethernet"
        self.srcMAC = ""
        self.dstMAC = ""
        self.ethernetType = None
        self.length = 0
        self.padding = bytes

    def DecodeFromBytes(self, data: bytes):
        """以太网数据包解码器"""
        self.srcMAC = data[0:6].hex(':')
        self.dstMAC = data[6:12].hex(':')
        self.ethernetType = GetBits(data[12:14],0,16)
        self.length = len(data)
        self.header = data[:14]
        self.payload = data[14:]

    @property
    def NextLayerType(self) -> str:
        return EthernetType(self.ethernetType).name


def DecodeEthernet(data: bytes, packet: Packet):
    eth = Ethernet()
    eth.DecodeFromBytes(data)
    packet.AddLayer(eth)
    packet.SetLinkLayer(eth)
    packet.NextDecoder(eth.NextLayerType)
