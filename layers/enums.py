from enum import Enum, auto


class BaseEnum(Enum):
    @classmethod
    def _missing_(cls, value: object):
        return cls.UNKNOWN  # type: ignore


# 以太网类型字段部分含义

# XXX使用枚举类型还是字典类型
class EthernetType(BaseEnum):
    IPv4 = 0x0800
    ARP = 0x0806
    SNMP = 0x814C
    IPv6 = 0x86DD
    LLDP = 0x86DD
    UNKNOWN = 0


ETHERNETTYPE = {
    0x0800: 'IPv4',
    0x0806: 'ARP',
    0x814C: 'SNMP',
    0x86DD: 'IPv6',
    0x88CC: 'LLDP',
}


class IPProtocol(BaseEnum):
    ICMPv4 = 1
    IGMP = 2
    IPv4 = 4
    TCP = 6
    UDP = 8
    IPv6 = 41
    ICMPv6 = 58
    UNKNOWN = 0


if __name__ == "__main__":
    print(IPProtocol(-1))
