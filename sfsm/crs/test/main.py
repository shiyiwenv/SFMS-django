# coding=utf-8
import json
import socket
import struct
import psutil

class CpuCollector(object):
    @staticmethod
    def get_base_info():
        info = {
            "cpu_count": psutil.cpu_count(),  # cpu物理核心数
            "cpu_freq": psutil.cpu_freq().max  # cpu最高频率
        }
        return info

class DiskCollector(object):
    def __init__(self):
        self.disk_part = []

    def get_base_info(self):
        self.disk_part = map(lambda x: dict(x._asdict()), psutil.disk_partitions())
        info = {
            "disk_part": self.disk_part,
            "disk_usage": map(lambda x: dict(psutil.disk_usage(x['mountpoint'])._asdict()), self.disk_part)
        }
        return info

class MemCollector(object):
    @staticmethod
    def get_base_info():
        info = {
            "phy_mem": dict(psutil.virtual_memory()._asdict()),
            "swap_mem": dict(psutil.swap_memory()._asdict())
        }
        return info

class NetWorkCollector(object):
    def __init__(self):
        self.inner_ips = {
            24: ip_to_int('10.255.255.255') >> 24,
            20: ip_to_int('172.31.255.255') >> 20,
            16: ip_to_int('192.168.255.255') >> 16
        }


    def _is_inner_ip(self, ip):
        ip_int = ip_to_int(ip)
        for bit, val in self.inner_ips.iteritems():
            if (ip_int >> bit) == val:
                return True
        return False

    def _get_ip_type(self, ip):
        if self._is_inner_ip(ip):
            return 'inner_net'
        elif ip in ('127.0.0.1',):
            return 'lo_net'
        else:
            return 'outer_net'

    def get_base_info(self):
        eth_info = {
            'inner_net': [],
            'outer_net': [],
            'lo_net': []
        }
        if_addr = psutil.net_if_addrs()
        for eth, net in if_addr.iteritems():
            ip = None
            for n in net:
                if n.family == 2 and n.address:
                    ip = n.address
                    break
            else:
                continue
            if ip is None:
                continue
            ip_type = self._get_ip_type(ip)
            eth_info[ip_type].append({'eth:': eth.decode('gbk'), 'ip_addr': ip})
        return eth_info

def ip_to_int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])


def int_to_ip(int_ip):
    return socket.inet_ntoa(struct.pack('I', socket.htonl(int_ip)))

def run():
    total = {}
    total.update(CpuCollector().get_base_info())
    total.update(MemCollector().get_base_info())
    total.update(DiskCollector().get_base_info())
    total.update(NetWorkCollector().get_base_info())
    return total

if __name__ == '__main__':
    print (json.dumps(run()))