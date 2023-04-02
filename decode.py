from layers.arp import DecodeARP
from layers.http import DecodeHTTP
from layers.ipv6 import DecodeIPv6
from layers.layer import Layer
from packet import Packet
from layers.ethernet import DecodeEthernet
from layers.ipv4 import DecodeIPv4
from layers.icmpv4 import DecodeICMPv4
from layers.tcp import DecodeTCP
from layers.udp import DecodeUDP
from layers.unknown import DecodeUnknown


# 解码器枚举
Decoder = {
    "Ethernet": DecodeEthernet,
    "IPv4": DecodeIPv4,
    "IPv6": DecodeIPv6,
    "ARP": DecodeARP,
    "ICMPv4": DecodeICMPv4,
    "TCP": DecodeTCP,
    "UDP": DecodeUDP,
    "HTTP":DecodeHTTP,
    "UNKNOWN": DecodeUnknown
}


# 解码器调用
def Decode(data: bytes, p: Packet, LayerType: str) -> bool:
    return Decoder[LayerType](data, p)


class PacketBuilder(Packet):
    '数据包层构建类'
    # 添加解析完成的层

    def __init__(self, contents: bytes) -> None:
        super().__init__()
        self.contents = contents

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
        if len(d) == 0 or len(next) == 0:
            return True
        if len(d) < 48 and int.from_bytes(d, "big") == 0:
            self.layers[0].padding = d
            return True
        Decode(d, self, next)

    # 获取包基本信息
    # XXX 需要优化逻辑
    def GetInfo(self):
        if len(self.info['summary']):
            return self.info['summary']
        info = {}
        if self.link:
            info['src'] = self.link.srcMAC
            info['dst'] = self.link.dstMAC

        if self.network:
            info['src'] = self.network.srcIP
            info['dst'] = self.network.dstIP

        info['protocol'] = self.last.__class__.__name__
        info['len'] = self.link.length
        info['info'] = self.last.Info
        self.info['summary'] = info
        return info

    # 获取包的详细信息
    def GetDetail(self):
        if len(self.info['detail']):
            return self.info['detail']
        detail = []
        for layer in self.layers:
            detail.append(layer.Detail)
        
        self.info['detail'] = detail
        return detail


# 开始数据包层解析链
def NewPacket(data: bytes, firstLayerDecoder: str, contents: bytes = b'') -> Packet:
    p = PacketBuilder(contents)
    p.data = data
    Decode(data, p, firstLayerDecoder)
    return p
