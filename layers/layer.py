from layers.base import BaseLayer


class Layer(BaseLayer):

    def __init__(self) -> None:
        super().__init__()

    # 解码本层数据
    def DecodeFromBytes(self, data: bytes):
        self.header = data

    # 获得下一层类型，默认为UNKNOWN
    @property
    def NextLayerType(self):
        return "UNKNOWN"
