# coding=utf-8

import psutil


class CpuCollector(object):
    @staticmethod
    def get_base_info():
        info = {
            "cpu_count": psutil.cpu_count(),  # cpu物理核心数
            "cpu_freq": psutil.cpu_freq().max  # cpu最高频率
        }
        return info
