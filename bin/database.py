#! /usr/bin/python

import configure
import MySQLdb
from DBUtils.PooledDB import PooledDB
from DBUtils.PooledDB import PooledDBError


def execute(sql, params):
	conn = ConnFactory.getConnection()
	cur = conn.cursor()
	cur.execute(sql, params)
	dataset = cur.fetchall()
	cur.close()
	conn.close()
	return dataset

class ConnFactory:

	conn_pool = None

	def __init__(self):
		if self.__class__ == ConnFactorty:
			raise NotImplementedError("abstract")
	
	@staticmethod
	def getConnection():
		if ConnFactory.conn_pool is None:
			conf = configure.getDbConfig()
			try:
				ConnFactory.conn_pool = PooledDB(creator=MySQLdb, \
					host=conf["host"],\
					port=conf["port"],\
					user=conf["user"],\
					passwd=conf["passwd"], 
					db=conf["db"])
			except PooledDBError as err:
				print("DB connection error!" + str(err))
				exit(1)

		return ConnFactory.conn_pool.connection()
