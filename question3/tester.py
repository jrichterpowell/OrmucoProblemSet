import socket 
import time

DELIM = '&&&&&'
#tests the cache Node
def sendCommand(cmd):
    sock.sendall(bytes(cmd + DELIM, encoding='utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 6556)) 
    sendCommand('dist|0|0')
    sendCommand('write|cow|1')
    sendCommand('write|dolphin|12')
    time.sleep(1)
    sendCommand('write|elephant|123')
    time.sleep(1)
    sendCommand('write|dog|1234')
    sendCommand('write|cat|12345')
    #should result in cow,do being removed
    sendCommand('write|tiger|123456')

    sendCommand('read|dolphin')
    print('waiting for result of read')
    data = sock.recv(1024)
    print("Value of dolphin is ", int.from_bytes(data, 'big'))

    #should result in elephant and not dolphin being bumped out, since we just accessed it
    sendCommand('write|lion|1234567')



