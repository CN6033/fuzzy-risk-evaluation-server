#! /usr/bin/env python
#coding=utf-8

__author__ = 'hstaos@gmail.com (Huang Shitao)'

import getopt
import sys
import logging
import daemon
import configure
import server


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:v", \
                ["help", "port=", "version"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for op, value in opts:
        if op == "-p":
            port = int(value)
            init()
            logging.info("Server is starting...")
            #with daemon.DaemonContext():
            server.start(port)
        elif op == "-v":
            print("Version:" + configure.get_conf()["version"])
        elif op == "-h":
            usage()


def usage():
    print("Use like this : ./fuzzyriskeval.py [-p port].")


def init():
    logging.basicConfig(filename=configure.get_conf()["log_file_path"],\
                        format='%(levelname)s %(asctime)s:%(message)s',\
                        level=logging.DEBUG)


if __name__ == "__main__":
    main()
