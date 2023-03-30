import libpcap as pcap
import ctypes
from collections import Callable


class WinPcapDevices(object):
    '获取所有网卡设备类'

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


class WinPcap(object):
    '访问WinPcap接口功能的类'
    # void packet_handler(u_char *param, const struct pcap_pkthdr *header, const u_char *pkt_data);
    HANDLER_SIGNATURE = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_ubyte),
                                         ctypes.POINTER(pcap.pkthdr),
                                         ctypes.POINTER(ctypes.c_ubyte))

    class WinPcapException(Exception):
        pass

    class CallbackIsNotCallable(WinPcapException):
        pass

    class DeviceIsNotOpen(WinPcapException):
        """
        Exception raised when trying to use the underlying device without opening it first.
        Can eb resolved by calling the sought method within a 'with' statement.
        """
        pass

    def __init__(self, device, snap_length=65536, promiscuous=1, timeout=1000) -> None:
        """_summary_

        Args:
            device (_type_): the name of the device to open on context enter.
            snap_length (int, optional): specifies the snapshot length to be set on the handle. Defaults to 65536.
            promiscuous (int, optional): specifies if the interface is to be put into promiscuous mode(0 or 1). Defaults to 1.
            timeout (int, optional): specifies the read timeout in milliseconds. Defaults to 1000.
        """
        self._handle = None
        self._device = device.encode('utf-8')
        self._snap_length = snap_length
        self._promiscuous = promiscuous
        self._timeout = timeout
        self._err_buffer = ctypes.create_string_buffer(
            pcap.PCAP_ERRBUF_SIZE + 1)
        self._callback = None
        self._callback_wrapper = self.HANDLER_SIGNATURE(self.packet_handler)

    def __enter__(self):
        assert self._handle is None
        self._handle = pcap.open_live(
            self._device, self._snap_length, self._promiscuous, self._timeout, self._err_buffer)
        return self

    def __exit__(self, type=None, value=None, trace=None):
        if self._handle is not None:
            pcap.close(self._handle)

    def packet_handler(self, param, header, pkt_pointer):
        if not isinstance(self._callback, Callable):
            raise self.CallbackIsNotCallable()
        pkt_data = ctypes.string_at(pkt_pointer, header.contents.len)
        return self._callback(self, param, header, pkt_data)

    def run(self, callback=None, limit=0):
        if self._handle is None:
            raise self.DeviceIsNotOpen()
        self._callback = callback
        pcap.loop(self._handle, limit, self._callback_wrapper, None)

    def stop(self):
        if self._handle is None:
            raise self.DeviceIsNotOpen()
        pcap.breakloop(self._handle)


if __name__ == "__main__":
    with WinPcapDevices() as devices:
        for device in devices:
            print(device.name, device.description)
