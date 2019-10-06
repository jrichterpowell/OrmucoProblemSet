import socket, time
from collections import OrderedDict
from threading import Thread

#Class that describes the client object
#It would be cool to also run a cache node inside the client

class CacheClient:
    def __init__(self,nodes,lite=True):
        self.distances = OrderedDict()
        self.nodes = nodes
        self.position = (0,0)

        self.writeQueue = []

        self.updateThread = Thread(target = self.update, args=())
        self.updateThread.start()
        
        #implement the internal cache
        if lite == True:
            pass
    
    #packs the string into our very simple message protocol
    def sendMessage(self, sock, msg):
        msgLen = len(msg) #works out nicely since utf-8 is 1 byte per char
        msgStr = b''.join([msgLen.to_bytes(8, 'big'), bytes(msg, encoding='utf-8')])
        sock.sendall(msgStr)
        return
    
    def rcvMessage(self, connection):
        #print("Node", self.name, 'Nothing in buffer, reading from socket', connection.getpeername())
        try:
            receivedB = connection.recv(8)
        except:
            return ''

        #get length of message from header
        readLen = int.from_bytes(receivedB, 'big')
        receivedB = connection.recv(readLen).decode('utf-8')

        #check if there's more to read than the socket provided
        if len(receivedB) < readLen:
            self.remainingToRead = readLen = receivedB
            return ''
        #else we got the whole message
        else:
            return receivedB

    
    #times responses from cacheNode's to determine the closest ones
    #we need to send our position since this is only simulated of course
    def getDistances(self):
        for nodeport in self.nodes:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1', nodeport))
                sock.settimeout(5)
                start = time.perf_counter()
                self.sendMessage(sock, 'dist|{}|{}'.format(str(self.position[0]), str(self.position[1])))
                try:
                    sock.recv(1024)
                except:
                    pass
                elapsed = time.perf_counter() -start
                self.distances[nodeport] = elapsed * 1000

        self.distances = OrderedDict(sorted(self.distances.items(), key=lambda item: item[1] ))

    #attempts to write messages that failed to write the first time
    def update(self):
        while True:
            time.sleep(60)
            for message in self.writeQueue:
                nodeport = message[0]
                key = message[1]
                value = message[2]
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect(('127.0.0.1', nodeport))
                        sock.settimeout(5)
                        self.sendMessage(sock, 'write|{}|{}'.format(key,value))

                        #check if the write was successful (adding 10 on sucess is a hack to remove that message on s)
                        if self.rcvMessage(sock):
                            message[3] = 10
                        else:
                            message[3] += 1
                except:
                    message[3] += 1
            
            #remove messages with more than 10 send attempts
            self.writeQueue = [m for m in self.writeQueue if m[3] < 10]


    #writes to ALL the cache nodes
    def writeCache(self, key, value):
        for nodeport in self.distances:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.connect(('127.0.0.1', nodeport))
                    sock.settimeout(5)
                    self.sendMessage(sock, 'write|{}|{}'.format(key,value))

                    #cache Node should acknowledge the write, if not, we store the message in a queue
                    if not self.rcvMessage(sock):
                        raise Exception
                except:
                    print("Client failed to send to", nodeport, key)
                    self.writeQueue += [[nodeport, key, value, 0]]

    
    #reads from only one of the cache nodes, does not update order in the others
    def readCache(self, key):
        #reads from the caches in order of increasing distance
        for nodeport in self.distances:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1', nodeport))
                #sock.settimeout(5)
                self.sendMessage(sock, 'read|' + key)
                response = self.rcvMessage(sock)

                if not response:
                    continue
                else:
                    return response
        return

    



    



        
