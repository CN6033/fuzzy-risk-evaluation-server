#!/usr/bin/env python
#coding=utf-8

'''
本模块实现作业的调度。
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'

import json
from dataproc import DataProc
import dbaccess


class JobControl:
    requests = []
    response = []

    def __init__(self, _request):
        request = json.loads(_request)
        self.requests = request["_data"]
        self.user = request["_user"]
        if not isinstance(self.requests, list):
            raise ValueError("There is no data in the request object!")

    def start(self):
        # If the request type is not 0, it means that the request data contains
        # nothing except the 'id' in the database.So we have to access the
        # database in order to get the rest of data by 'id'.
        for req in self.requests:
            if req["_type"] != 0:
                req = self._get_data_from_db(req["_id"], self.user)
            else:
                self._store_data_to_db(req, self.user)

            try:
                proc = DataProc(req)
                res = proc.start()
                res["vid"] = req["_id"]
                self.response.append(res)
            except ValueError:
                pass
            finally:
                return json.dumps(self.response)

    def _get_data_from_db(self, _id, _user):
        dataset = dbaccess.get_data(_id, _user)
        return json.loads(dataset[0][1])

    def _store_data_to_db(self, _req, _user):
        dbaccess.store_data(_req, _user)
