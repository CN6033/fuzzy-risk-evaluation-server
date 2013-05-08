#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'


import ConfigParser
import logging


DB_CONF_PATH = '../conf/db.conf'
MAIN_CONF_PATH = '../conf/main.conf'


def get_db_config():
	'''Get the database connection configure'''
	conf = {}
	try:
		config = ConfigParser.RawConfigParser()
		config.read(DB_CONF_PATH)
		conf["host"] = config.get('mysqld', 'host')
		conf["user"] = config.get('mysqld', 'user')
		conf["passwd"] = config.get('mysqld', 'passwd')
		conf["db"] = config.get('mysqld', 'db_name')
		conf["port"] = config.getint('mysqld', 'port')
		conf["dbapi"] = config.get('mysqld', 'dbapi')
		conf["mincached"] = config.getint('mysqld', 'mincached')
		conf["maxcached"] = config.getint('mysqld', 'maxcached')

	except IOError as err:
		logging.error("Exception happened when reading the db configuration file: conf/db.conf!" + str(err))
		exit(1)

	return conf


def get_conf():
	'''Get the main process' configuration.'''
	conf = {}
	try:
		config = ConfigParser.RawConfigParser()
		config.read(MAIN_CONF_PATH)
		conf["log_file_path"] = config.get('main', 'log_file_path')
		conf["port"] = config.get('server', 'port')
		conf["version"] = config.get('main', 'version')
	except IOError as err:
		logging.error("Exception happened when reading the main configuration file: conf/main.conf!" + str(err))
		exit(1)
	return conf
