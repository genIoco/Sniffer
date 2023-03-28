class BaseLayer(object):
    '网络数据包基类'

    def __init__(self) -> None:
        # 本层数据包头部
        self.header = bytes()
        # 本层数据包数据部分
        self.payload = bytes()

    # 返回本层头部原始信息
    def LayerHeader(self):
        return self.header

    # 返回本层数据段原始信息
    def LayerPayload(self):
        return self.payload

    # 返回数据包的字符串形式
    def String(self):
        str = ""
        for c in self.header+self.payload:
            if c in range(32, 127):
                str += chr(c)
            else:
                str += '.'
        return str

    # 返回数据包的十六进制转储
    def Dump(self):
        # return " ".join("{:02x}".format(c) for c in self.header+self.payload)
        return (self.header+self.payload).hex(' ')
