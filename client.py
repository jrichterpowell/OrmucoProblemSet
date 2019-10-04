import socket, time
from collections import OrderedDict

#Class that describes the client object
#Can be implemented in either a lite manner, where it solely makes requests to the other cache nodes
#or it can contain a cache itself (it memory is sufficient) to further improve lookup time

class CacheClient:
    def __init__(self,nodes,lite=True):
        self.distances = OrderedDict()
        self.nodes = nodes
        self.sockets = {}
        self.DELIM ='&&&&&'
        
        #implement the internal cache
        if lite == True:
            pass
    
    def sendCommand(self, sock, cmd):
        sock.sendall(bytes(cmd + self.DELIM, encoding='utf-8'))

    
    def getDistances(self):
        for nodeport in self.nodes:
            if not nodeport in self.sockets.keys():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', nodeport))
                self.sockets[nodeport] = sock
            else:
                sock = self.sockets[nodeport]

            start = time.perf_counter()
            self.sendCommand(sock, 'dist|0|0')
            sock.recv(1024)
            elapsed = time.perf_counter() -start
            print(elapsed)
            self.distances[nodeport] = elapsed * 1000

        self.distances = OrderedDict(sorted(self.distances.items(), key=lambda item: item[1] ))

    #writes to ALL the cache nodes
    def writeCache(self, key, value):
        for node in self.distances:
            sock = self.sockets[node]
            self.sendCommand(sock, 'write|{}|{}'.format(key,value))
    
    #reads from only one of the cache nodes, does not update order in the others
    def readCache(self, key):
        for node in self.distances:
            sock = self.sockets[node]
            self.sendCommand(sock, 'read|' + key)
            response = sock.recv(1024)
            if not response:
                continue
            else:
                return int.from_bytes(response, 'big')
        
        return

    def destroySockets(self):
        for socket in self.sockets.values():
            socket.close()
    



    



        