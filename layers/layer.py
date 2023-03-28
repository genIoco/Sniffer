from layers.base import BaseLayer


class Layer(BaseLayer):

    # 解码本层数据
    def DecodeFromBytes(self, data: bytes):
        pass
    
    # 获得下一层类型
    @property
    def NextLayerType(self):
        pass

