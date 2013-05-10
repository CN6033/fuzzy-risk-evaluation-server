#! /usr/bin/env python
#coding=utf-8

'''
本模块实现数据库连接管理和SQL语句执行功能。

本模块接口：
    execute(sql, params)
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'

import configure
import MySQLdb
from DBUtils.PooledDB import PooledDB
from DBUtils.PooledDB import PooledDBError


class execute():

    def __init__(self, sql, params):
        self.sql = sql
        self.params = params

    def __enter__(self):
        self.conn = ConnFactory.getConnection()
        self.cur = self.conn.cursor()
        self.cur.execute(self.sql, self.params)
        dataset = self.cur.fetchall()
        return dataset

    def __exit__(self, _type, _value, _traceback):
        self.cur.close()
        self.conn.close()


class ConnFactory:

    conn_pool = None

    def __init__(self):
        if self.__class__ == ConnFactorty:
            raise NotImplementedError("abstract")

    @staticmethod
    def getConnection():
        if ConnFactory.conn_pool is None:
            conf = configure.get_db_config()
            try:
                ConnFactory.conn_pool = PooledDB(creator=MySQLdb, \
                    host=conf["host"],\
                    port=conf["port"],\
                    user=conf["user"],\
                    passwd=conf["passwd"],\
                    db=conf["db"],\
                    charset="utf8")
            except PooledDBError as err:
                print("DB connection error!" + str(err))
                exit(1)

        return ConnFactory.conn_pool.connection()
