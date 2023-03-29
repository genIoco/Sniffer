import libpcap as pcap
import ctypes


class WinPcapDevices(object):
    '网卡设备类'

    def __init__(self) -> None:
        self._all_devices = None

    def __enter__(self):
        assert self._all_devices is None
        all_devices = ctypes.POINTER(pcap.pcap_if_t)()
        err_buffer = ctypes.create_string_buffer(pcap.PCAP_ERRBUF_SIZE + 1)
        pcap.findalldevs(ctypes.byref(all_devices), err_buffer)
        self._all_devices = all_devices
        return self

    def __exit__(self, type, value, trace):
        if self._all_devices is not None:
            pcap.freealldevs(self._all_devices)

    def interface_iterator(self):
        if self._all_devices is None:
            raise StopIteration
        device = self._all_devices
        while device:
            yield device.contents
            device = device.contents.next

    def __iter__(self):
        return self.interface_iterator()


if __name__ == "__main__":
    with WinPcapDevices() as devices:
        for device in devices:
            print(device.name, device.description)
