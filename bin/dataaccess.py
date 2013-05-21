#! /usr/bin/env python
#coding=utf-8

'''
本模块实现从原始数据转换成'dataproc'模块所需格式数据的功能。
同时，也提供了原始数据完整性和正确性的检查（注：此功能暂未完全实现）。
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'


import logging


class DataAccess:

    def __init__(self, _raw):
        if 0 > check(_raw):
            logging.warning("The raw data is bad.")
            raise ValueError("The raw data is bad.")
        self.raw = _raw

    def get_level_data(self):
        data = []
        for _level in self.raw["_def"]["_level"]:
            data.append((_level["_id"], _level["_pid"]))
        return data

    def get_evals(self):
        data = []
        for _eval in self.raw["_res"]["_eval"]:
            data.append((_eval["_level_id"], _eval["_class_id"]))
        return data

    def get_classes(self):
        data = []
        for _class in self.raw["_def"]["_class"]:
            data.append((_class["_id"], _class["_value"]))
        return data

    def get_weight_result(self):
        data = []
        for _weight in self.raw["_res"]["_weight"]:
            data.append((_weight["_level_id1"], _weight["_level_id2"], _weight["_value"]))
        return data


def check(raw):
    '''检查原始数据的正确性和完整性'''
    if raw is None:
        return -1
    try:
        if None == raw["_def"]["_level"]:
            return -1
        if None == raw["_def"]["_class"]:
            return -1
        if None == raw["_res"]["_eval"]:
            return -1
        if None == raw["_res"]["_weight"]:
            return -1
    except:
        return -1
    return 0
