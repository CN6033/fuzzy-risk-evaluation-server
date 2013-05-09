#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'

'''
This module implements the job control.
'''

import json
from dataproc import DataProc
import dbaccess

class JobControl:
    reqs = []
    response = {}

    def __init__(self, _request):
        request = json.loads(_request)
        reqs = request["_data"]
        self.user = request["_user"]
        response = []
        if not isinstance(reqs, list):
            raise ValueError("There is no data in the requst object!")


    def start(self):
        # If the request type is not 0, it means that the request data contains nothing 
        # except the 'id' in the database.
        # So we have to access the database in order to get the rest of data by 'id'.
        for req in reqs:
            if req["_type"] != 0:
                req = _get_data_from_db(req["_id"], self.user)
            else:
                _store_data_to_db(req, self.user)
            
	        try:
                proc = DataProc(req)
                res = proc.start()
                res["vid"] = req["_id"]
                response.append(res)
            except ValueError:
                pass
            finally:
                return json.dumps(response)
	
    def _get_data_from_db(self, _id, _user):
        dataset = dbaccess.get_data(_id, _user)
        return json.loads(dataset[0][1])

    def _store_data_to_db(self, _req, _user):
        dbaccess.store_data(_req, _user)
