import socket,random, time

class Node:

    def __init__(self, cap, name='alpha', port=6555, position=(0,0)):
        self.store = dict()
        self.ttl = 3 #objects in cache live for 3 minutes
        self.cap = cap
        self.size = 0
        self.delim = '&&&&&'
        self.port = port
        self.position = position
        self.name = name

        #keep track of the most and least recently used keys 
        self.order = []

    def respondToPing(self, x, y):
        #waits for an amount corresponding to the distance between this node and the pinger, 
        #in order to simulate network latency
        distance = (x - self.position[0])**2 + (y - self.position[1])**2
        print("Distance from origin: ", distance, "for node", self.name)
        time.sleep(distance / 1000)
        return 

    def dropLRU(self):
        LRU = self.order.pop()
        print("Deleting LRU item:", LRU, self.store[LRU])
        self.size -= 1
        del self.store[LRU]
        return

    #writes to a cache location
    def writeToCache(self, key, value):
        if key in self.store.keys():
            self.store[key] = value
            #we know the key has to be in the usage order array, since it's already in the cache
            self.order.remove(key)
            self.order.insert(0, key)
        else:
            if self.size == self.cap:
                self.dropLRU()
            self.store[key] = value
            self.size += 1
            self.order.insert(0, key)

    #returns the object if the key is in the dictionary, otherwise returns none
    def readFromCache(self, key):
        if key in self.store.keys():
            #make this the most recently used key and return
            self.order.remove(key)
            self.order.insert(0, key)
            return self.store[key]
        else:
            return None

    def serve(self):
        print("Running node")
        #simple socket server which returns the requested cache element if it exist
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', self.port))
            sock.listen()
            connection, addr = sock.accept()
            while True: 
                requests = repr(connection.recv(4096))[2:-1] #drop the bytes prefix and 
                if not requests:
                    continue
                print("Node", self.name, "receved: ", requests.replace(self.delim, ''))
                for request in requests.split(self.delim):
                    if request == '':
                        continue
                    reqArgs = request.split('|')
                    print(reqArgs)
                    if reqArgs[0] == "dist":
                        latency = self.respondToPing(int(reqArgs[1]), int(reqArgs[2]))
                        connection.sendall(b'pong')
                    elif reqArgs[0] == "write":
                        self.writeToCache(reqArgs[1], int(reqArgs[2]))
                        #connection.sendall(bytes('Wrote {} to {}'.format(reqArgs[2],reqArgs[1]), encoding='utf-8'))
                    elif reqArgs[0] == 'read':
                        item = self.readFromCache(reqArgs[1])
                        if item:
                            connection.sendall(item.to_bytes(8, "big"))
                        else:
                            connection.sendall(b"Key Not Found")
                    else:
                        connection.sendall(b"Request Not Understood")
                time.sleep(1)