# coding=utf-8
import socket
import struct


def trans_size(size):
    pass


def ip_to_int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])


def int_to_ip(int_ip):
    return socket.inet_ntoa(struct.pack('I', socket.htonl(int_ip)))
