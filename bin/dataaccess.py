#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'


'''
This module check whether the raw data's form is correct,
And transform the raw data form in order to match the  'dataproc' module needs.
'''

import logging

class DataAccess:
    def __init__(self, _raw):
        if 0 > check(_raw):
            logging.warning("The raw data is bad.")
            raise ValueError("The raw data is bad.")
        self.raw = _raw

    
    def get_level_data():
        for _level in self.raw["_def"]["_level"]:
            yield (_level["_id"], _level["_pid"])


    def get_evals():
        for _eval in self.raw["_res"]["_eval"]:
            yield (_eval["_level_id"], _eval["_class_id"])


    def get_classes():
        for _class in self.raw["_def"]["_class"]:
            yield (_class["_id"], _class["_value"])


    def get_weight_result():
        for _weight in self.raw["_res"]["_weight"]:
            yield (_weight["_level_id1"], _weight["_level_id2"], _weight["_value"])


def check(raw):
    '''Check the data before calculate.'''
    if raw is None:
       return -1
    try:
        if None == self.raw["_def"]["_level"]:
            return -1
        if None == self.raw["_def"]["_class"]:
            return -1
        if None == self.raw["_res"]["_eval"]:
            return -1
        if None == self.raw["_res"]["_weight"]:
            return -1
    except:
        return -1
    
    return 0

