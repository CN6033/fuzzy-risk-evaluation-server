#! /usr/bin/env python
#coding=utf-8

# 本模块实现配置文件的读取功能。
# 主要的配置文件有：db.conf和main.conf。
# 在db.conf中保存着数据库相关的配置信息，
# 而与主程序相关的配置都保存在main.conf中。

__author__ = 'hstaos@gmail.com (Huang Shitao)'


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
        logging.error("Exception happened when reading the db configuration file: conf/db.conf!" \
            + str(err))
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
        logging.error("Exception happened when reading the main configuration file: conf/main.conf!"\
            + str(err))
        exit(1)
    return conf
