
from layers.base import BaseLayer
from layers.layer import Layer


class Packet:
    '数据包层构建虚基类'

    def __init__(self) -> None:
        self.data = bytes()
        self.layers = []
        self.last = BaseLayer()
        self.link = None
        self.network = None
        self.transport = None
        self.application = None
        self.info = {'summary': {},
                     'detail': []}
        self.stream = {}

    # 返回数据包字符串形式
    def String(self):
        str = ""
        for c in self.data:
            if c in range(32, 127):
                str += chr(c)
            else:
                str += '.'
        return str

    # 返回数据包的十六进制转储
    def Dump(self):
        return self.data.hex(' ')

    # 添加解析完成的层
    def AddLayer(self, layer: Layer):
        pass

    # 设置链路层协议
    def SetLinkLayer(self, layer: Layer):
        pass

    # 设置网络层协议
    def SetNetworkLayer(self, layer: Layer):
        pass

    # 设置传输层协议
    def SetTransportLayer(self, layer: Layer):
        pass

    # 设置应用层协议
    def SetApplicationLayer(self, layer: Layer):
        pass

    # 调用下一层解码器
    def NextDecoder(self, next):
        pass
