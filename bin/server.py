#! /usr/bin/env python
#coding=utf-8

'''
本模块主要完成网络I/O。
使用了Epoll + 多线程模型来提高TCP并发连接数
'''

__author__ = 'hstaos@gmail.com (Huang Shitao)'

import socket
import select
import threading
import logging
import jobcontrol


def start(port = 8000):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', port))
    serversocket.listen(1)
    serversocket.setblocking(0)

    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

    try:
        connections = {}
        requests = {}
        responses = {}
        __closeConn = disconnect(requests, responses, epoll, connections)
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
                    is_conn_close = False
                    try:
                        while True:
                            data = connections[fileno].recv(1024)
                            requests[fileno] += data
                            if len(data) == 0:
                                #Shutdown the connection!
                                #epoll.modify(fileno, select.EPOLLET)
                                #connections[fileno].shutdown(socket.SHUT_RDWR)
                                __closeConn(fileno)
                                is_conn_close = True
                                break
                    except:
                        # The except occur only at the time when receved all of the data.
                        pass

                    try:
                        if is_conn_close is False:
                            thread = threading.Thread(target=proc, \
                                    args=(requests, responses, epoll, fileno, __closeConn))
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
                    __closeConn(fileno)
                    #epoll.unregister(fileno)
                    #connections[fileno].close()
                    #del connections[fileno]
    except:
        pass
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()


def proc(requests, responses, epoll, fileno, __closeConn):
    try:
        try:
            job = jobcontrol.JobControl(requests[fileno])
            result = job.start()
            responses[fileno] = result
        except ValueError as verr:
            logging.warning(verr)
            responses[fileno] = 'Empty data!'
        requests[fileno] = b''
        epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
    except:
        #When the client shutdown connection before results send back, this exception will occur.
        logging.warning("The client shutdown the connection before the results send back.")
        __closeConn(fileno)


def disconnect(requests, responses, epoll, connections):

    def __closeFunc(fileno):
        try:
            epoll.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
            del requests[fileno]
            del responses[fileno]
        except:
            pass
    return __closeFunc


if __name__ == "__main__":
    start(8004)
