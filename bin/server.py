#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'

import socket, select, threading, logging, time

def start(port = 8000):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind(('0.0.0.0', port))
	serversocket.listen(1)
	serversocket.setblocking(0)

	epoll = select.epoll()
	epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

	try:
		connections = {}; requests = {}; responses = {}
		while True:
			events = epoll.poll(50)
			for fileno, event in events:
				if fileno == serversocket.fileno():
					try:
						while True:
							connection, address = serversocket.accept()
							connection.setblocking(0)
							epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
							connections[connection.fileno()] = connection
							requests[connection.fileno()] = b''
							responses[connection.fileno()] = b''
					except socket.error:
						pass
				elif event & select.EPOLLIN:
					_conn_close = 0
					try:
						while True:
							data = connections[fileno].recv(1024)
							requests[fileno] += data
							if len(data) == 0: 
								#Shutdown the tcp connection!
								epoll.modify(fileno, select.EPOLLET)
								connections[fileno].shutdown(socket.SHUT_RDWR)
								_conn_close = 1
								break
					except: 
						# The except occur only at the time when receved all of the data.
						pass
					
					try:
						if _conn_close == 0:
							thread = threading.Thread(target=proc, \
									args=(requests, responses, epoll, fileno))
							thread.start()
					except RuntimeError as err:
						logging.exception("RuntimeError: " + str(err))

				elif event & select.EPOLLOUT:
					try:
						while len(responses[fileno]) > 0:
							byteswritten = connections[fileno].send(responses[fileno])
							responses[fileno] = responses[fileno][byteswritten:]
					except socket.error:
						pass

					if len(responses[fileno]) == 0:
						epoll.modify(fileno, select.EPOLLIN | select.EPOLLET)
						#connections[fileno].shutdown(socket.SHUT_RDWR)
				elif event & select.EPOLLHUP:
					disconnect(requests, responses, epoll, connections, fileno)
					#epoll.unregister(fileno)
					#connections[fileno].close()
					#del connections[fileno]
	except:
		pass
	finally:
		epoll.unregister(serversocket.fileno())
		epoll.close()
		serversocket.close()

def proc(requests, responses, epoll, connections, fileno):
	time.sleep(3)
	responses[fileno] = requests[fileno]
	requests[fileno] =  b''
	try:
		epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
	except ValueError as err: 
		#When the client shutdown connection before results send back, this exception will occur.
		logging.warning(str(err))
		disconnect(requests, responses, epoll, connections, fileno)

def disconnect(requests, responses, epoll, connections, fileno):
	try:
		connections[fileno].close()
	finally:
		epoll.unregister(fileno)
		del connections[fileno]
		del requests[fileno]
		del responses[fileno]

def fuzzyRiskEval(data):
	g_level_tree = dataproc.buildLevelTree(data)
	dataproc.setValue2LevelTree(data, g_level_tree)
	dataproc.calculateAndSetWeight2LevelTree(data, g_level_tree)
	g_B = dataproc.fuzzySyntheticEvaluation(data, g_level_tree)
	print(dataproc.calculateFinalScore(data, g_B))

if __name__ == "__main__":
	start(8001)
