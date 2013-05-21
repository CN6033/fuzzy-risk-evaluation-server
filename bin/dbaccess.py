#! /usr/bin/env python
#coding=utf-8

'''
# 本模块实现数据的持久化。
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'

from database import execute
import uuid
import json


def get_data(v_id, user):
    if v_id is None:
        return None
    sql = "SELECT t1.vid, t1.data"\
           + " FROM t_data t1, t_user t2, t_user_data t3"\
           + " WHERE t2.username = %s"\
           + " AND t2.id = t3.userid"\
           + " AND t1.id = t3.dataid"\
           + " AND t1.vid = %s"
    params = (user, str(v_id))
    with execute(sql, params) as dataset:
        return dataset


def store_data(req, user):
    req["_id"] = generate_vid()
    req_str = json.dumps(req)
    sql = "START TRANSACTION;"\
        + "INSERT INTO t_data(vid, data) VALUES(%s, %s);"\
        + "SELECT @A:= LAST_INSERT_ID();"\
        + "INSERT INTO t_user_data (userid, dataid) SELECT id, @A "\
        + "FROM t_user WHERE username = %s;"\
        + "COMMIT;"
    params = (req["_id"], req_str, user)
    with execute(sql, params):
        pass


def generate_vid():
    '''给每次评估生成一个唯一的ID.'''
    return str(uuid.uuid1().int)
