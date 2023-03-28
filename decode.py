from layers.arp import DecodeARP
from layers.layer import Layer
from packet import Packet
from layers.ethernet import DecodeEthernet
from layers.ipv4 import DecodeIPv4
from layers.tcp import DecodeTCP
from layers.udp import DecodeUDP
from layers.unknown import DecodeUnknown


# 解码器枚举
Decoder = {
    "Ethernet": DecodeEthernet,
    "IPv4": DecodeIPv4,
    "ARP": DecodeARP,
    "TCP": DecodeTCP,
    "UDP": DecodeUDP,
    "UNKNOWN": DecodeUnknown
}


# 解码器调用
def Decode(data: bytes, p: Packet, LayerType: str) -> bool:
    return Decoder[LayerType](data, p)


class PacketBuilder(Packet):
    '数据包层构建类'
    # 添加解析完成的层

    def __init__(self) -> None:
        super().__init__()

    def AddLayer(self, layer: Layer):
        self.layers.append(layer)
        self.last = layer

    # 设置链路层协议
    def SetLinkLayer(self, layer: Layer):
        if self.link == None:
            self.link = layer

    # 设置网络层协议
    def SetNetworkLayer(self, layer: Layer):
        if self.network == None:
            self.network = layer

    # 设置传输层协议
    def SetTransportLayer(self, layer: Layer):
        if self.transport == None:
            self.transport = layer

    # 设置应用层协议
    def SetApplicationLayer(self, layer: Layer):
        if self.application == None:
            self.application = layer

    # 调用下一层解码器
    def NextDecoder(self, next):
        d = self.last.LayerPayload()
        if len(d) == 0:
            return True
        # XXX 优化填充判断逻辑
        if len(d) < 48 and int.from_bytes(d, "big") == 0:
            self.layers[0].padding = d
            return True
        Decode(d, self, next)


# 开始数据包层解析链
def NewPacket(data: bytes, firstLayerDecoder: str) -> Packet:
    p = PacketBuilder()
    p.data = data
    Decode(data, p, firstLayerDecoder)
    return p
