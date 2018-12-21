# coding=utf-8
import psutil


class MemCollector(object):
    @staticmethod
    def get_base_info():
        info = {
            "phy_mem": dict(psutil.virtual_memory()._asdict()),
            "swap_mem": dict(psutil.swap_memory()._asdict())
        }
        return info