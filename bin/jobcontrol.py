#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'

import json
from dataproc import DataProc


class JobControl:
    reqs = []
    response = {}

    def __init__(self, _request):
        self.request = json.loads(_request)
        reqs = self.request["_data"]
        if not isinstance(reqs, list):
            raise ValueError("There is no data in the requst object!")


    def start(self):
        for req in reqs:
	        try:
                proc = DataProc(req)
                res = proc.start()
            except ValueError:
                pass
	
    
