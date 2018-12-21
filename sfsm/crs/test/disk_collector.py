# coding=utf-8

import psutil


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
