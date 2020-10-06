'''
    2非阻塞
'''
#!/usr/bin/env python 
# encoding: utf-8

import socket 
def nonblocking_way():
    sock = socket.socket() 
    sock.setblocking(False)
    try:
        sock.connect(('www.douban.com',80))
    except BlockingIOError:
        pass

    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    data = request.encode('ascii')
    while True:
        try:
            sock.send(data)
            break
        except OSError:
            pass
    
    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk 
                chunk = sock.recv(4096)
            break
        except OSError:
            pass

    return response

def sync_way():
    res = []
    for i in range(10):
        res.append(nonblocking_way())
    return len(res)

if __name__=='__main__':
    import time
    main()