#! /usr/bin/python

import ConfigParser

def getDbConfig():
#Get the database connect configure
	conf = {}
	try:
		config = ConfigParser.RawConfigParser()
		config.read('../conf/db.conf')
		conf["host"] = config.get('mysqld', 'host')
		conf["user"] = config.get('mysqld', 'user')
		conf["passwd"] = config.get('mysqld', 'passwd')
		conf["db"] = config.get('mysqld', 'db_name')
		conf["port"] = config.getint('mysqld', 'port')
		conf["dbapi"] = config.get('mysqld', 'dbapi')
		conf["mincached"] = config.getint('mysqld', 'mincached')
		conf["maxcached"] = config.getint('mysqld', 'maxcached')

	except IOError as err:
		print("IOError: " + str(err))
		exit(1)
		
	return conf
