# coding=utf-8
import psutil

from utils import ip_to_int


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