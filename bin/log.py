#! /usr/bin/python3

class Log:
	def getLogFile():
		#打开或创建log/log日志文件；返回文件描述符。
		print("getLogFile")

	def getWfLogFile():
		#打开或创建log/log.wf日志文件；返回文件描述符。
		print("getWfLogFile")

	def w2log(info):
		#写入日志文件
		print("w2log" + str(info))


	def w2wflog(info):
		#写入错误或警告日志文件
		print("w2wflog" + str(info))
