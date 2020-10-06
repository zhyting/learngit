'''
主要是对 generator.py 的抽象，两者基本相同
https://github.com/denglj/aiotutorial/blob/master/part_1/yieldfrom.py

可能在程序只完成之前，文件描述法还是注册在select中的
'''

#!/usr/bin/env python 
# encoding: utf-8 

import socket 
import selectors import DefaultSelector,EVENT_WRITE,EVENT_READ

stopped = False
urls_todo = {'/','/1','/2','/3','/4','/5','/6','/7','/8','/9'}

def connect(sock,address):
    f = Future()
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass

    def on_connected():
        f.set_result(None)

    selector.register(sock.fileno(),EVENT_WRITE,on_connected)
    yield from f 
    selector.unregister(sock.fileno())
    

def read(sock):
    f = Future() 

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(),EVENT_READ,on_readable)
    chunk = yield from f 
    selector.unregister(sock.fileno())
    return chunk

def read_all(sock):
    response = []
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
    return b''.join(response) 


class Future:
    def __init__(self):
        self.result = None
        self._callback = []

    def add_done_callback(self,fn):
        self._callbacks.append(fn)

    def set_result(self,result):
        self.result = result 
        for fn in self._callback:
            fn(self)
        
    def __iter__(self):
        yield self
        return self.result 

class Crawler:
    def __init__(self,url):
        self.url = url
        self.response = b''

    def fetch(self):
        global stopped 
        sock = socket.socket()
        yield from connect(sock, ('www.douban.com',80))
        get = 'GET {0} HTTP/1.0\r\nHost: www.douban.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True

class Task:
    def __init__(self,coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self,Future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return 
        next_future.add_done_callback(self.step)


def loop():
    while not stopped:
        events = selectors.select() 
        for event_key,event_mask in events:
            callback = event_key.data
            callback() 

if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())
    loop() 
    print(time.time() - start)