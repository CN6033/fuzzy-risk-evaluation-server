#!/usr/bin/env python

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'

import socket, select, threading, logging

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
			events = epoll.poll(20)
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
					try:
						while True:
							data = connections[fileno].recv(1024)
							if not data: 
								break
							requests[fileno] += data
					except socket.error:
						pass

					try:
						thread = threading.Thread(target=proc, \
								args=(requests, responses, epoll, fileno))
						thread.start()
						#epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
					except RuntimeError:
						print "Thread runtime error!"

				elif event & select.EPOLLOUT:
					try:
						while len(responses[fileno]) > 0:
							byteswritten = connections[fileno].send(responses[fileno])
							responses[fileno] = responses[fileno][byteswritten:]
					except socket.error:
						pass
					if len(responses[fileno]) == 0:
						epoll.modify(fileno, select.EPOLLET)
						connections[fileno].shutdown(socket.SHUT_RDWR)
				elif event & select.EPOLLHUP:
					epoll.unregister(fileno)
					connections[fileno].close()
					del connections[fileno]
	except:
		pass
	finally:
		epoll.unregister(serversocket.fileno())
		epoll.close()
		serversocket.close()

def proc(requests, responses, epoll, fileno):
	responses[fileno] = requests[fileno]
	epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)

if __name__ == "__main__":
	start()
