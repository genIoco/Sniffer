import socket


# 二进制流的转换
def GetBits(data, start: int, num: int) -> int:  # type: ignore
    """获取字节中的某几位二进制数据"""
    if isinstance(data, bytes):
        length = len(data)*8
        data = int.from_bytes(data, "big")
    else:
        length = 8

    key = 1
    for _ in range(num):
        key <<= 1
        key += 1
    data >>= (length - start - num)
    return data & key


def BytesEncode(x):
    """确保给定的数据位字节流"""
    if isinstance(x, str):
        return x.encode()
    return bytes(x)


def InetNtop(af: int, addr: bytes) -> str:
    """将IP地址从二进制转换为字符串形式"""
    addr = BytesEncode(addr)
    try:
        return socket.inet_ntop(af, addr)
    except KeyError:
        raise ValueError("unknown address family %d" % af)


if __name__ == "__main__":
    data = b'\xff\x02\x03'
    print(bin(GetBits(data, 0, 24)))
