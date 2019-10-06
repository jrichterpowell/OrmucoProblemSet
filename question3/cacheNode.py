import socket,random, time, selectors

class Node:
    def __init__(self, cap, name='alpha', port=6555, position=(0,0),lock=None):
        self.store = dict()
        self.ttl = 0.25 #objects in cache live for 15 seconds
        self.cap = cap
        self.size = 0
        self.port = port
        self.position = position
        self.name = name

        self.printlock = lock

        #keep track of the most and least recently used keys 
        self.order = []

    def safePrint(self, *args):
        with self.printlock:
            print(*args, flush=True)

    def cleanCache(self):
        #get the current time, remove entries that are older than the time to live
        curtime = time.time()
        keys = list(self.store.keys())
        for key in keys:
            if self.store[key][1] + (60*self.ttl) < curtime:
                self.safePrint("Node", self.name, "Removed stale entry:", key)
                self.order.remove(key)
                del self.store[key]


    def respondToPing(self, x, y):
        #waits for an amount corresponding to the distance between this node and the pinger, 
        #in order to simulate network latency
        distance = (x - self.position[0])**2 + (y - self.position[1])**2
        self.safePrint("Distance from origin: ", distance, "for node", self.name)
        time.sleep(distance / 1000)
        
        return 

    #packs the string into our very simple message protocol
    def sendMessage(self, sock, msg):
        msgLen = len(msg) #works out nicely since utf-8 is 1 byte per char
        msgStr = b''.join([msgLen.to_bytes(8, 'big'), bytes(msg, encoding='utf-8')])
        try:
            sock.sendall(msgStr)
        except:
            pass
        return
    
    def rcvMessage(self, connection):
        try:
            receivedB = connection.recv(8)
        except:
            return ''

        #get length of message from header 
        readLen = int.from_bytes(receivedB, 'big')
        receivedB = connection.recv(readLen).decode('utf-8')

        #check if there's more to read than the socket provided
        if len(receivedB) < readLen:
            self.safePrint("Error reading ")
        #else we got the whole message
        else:
            return receivedB

    def dropLRU(self):
        LRU = self.order.pop()
        self.safePrint("Deleting LRU item:", LRU, self.store[LRU])
        self.size -= 1
        del self.store[LRU]
        return

    #writes to a cache location
    def writeToCache(self, key, value):
        curtime = time.time()
        if key in self.store.keys():
            self.store[key] = (value,curtime)
            #we know the key has to be in the usage order array, since it's already in the cache
            self.order.remove(key)
            self.order.insert(0, key)
        else:
            if self.size == self.cap:
                self.dropLRU()
            self.store[key] = (value,curtime)
            self.size += 1
            self.order.insert(0, key)
    
    #returns the object if the key is in the dictionary, otherwise returns none
    def readFromCache(self, key):
        if key in self.store.keys():
            #make this the most recently used key and return
            self.order.remove(key)
            self.order.insert(0, key)

            #update the last accesed time
            self.store[key] = (self.store[key][0], time.time())
            return self.store[key][0]
        else:
            return None

    def respond(self, sel, key, mask):
        connection = key.fileobj

        if not mask & selectors.EVENT_READ:
            return 
        request = self.rcvMessage(connection)

        if not request:
            return

        self.safePrint("Node", self.name, "received: ", request)
        reqArgs = request.split('|')

        if reqArgs[0] == "dist":
            self.respondToPing(int(reqArgs[1]), int(reqArgs[2]))
            self.sendMessage(connection, 'pong')

        elif reqArgs[0] == "write":
            #reply that write was successful
            if self.writeToCache(reqArgs[1], reqArgs[2]):
                self.sendMessage(connection, 'Write succesful')
            else:
                self.sendMessage(connection, 'Write failed. Value is either too long or there was a socket error')
        elif reqArgs[0] == 'read':
            item = self.readFromCache(reqArgs[1])
            if item:
                self.sendMessage(connection, item)
            else:
                self.sendMessage(connection, "Key Not Found")
        else:
            self.sendMessage(connection, "Request Not Understood")

    def handleNewConn(self, sel, key, mask):
        connection, _ = key.fileobj.accept()
        connection.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(connection, events, data=self.respond)

    def serve(self):
        self.safePrint("Running node")
        #simple socket server which returns the requested cache element if it exist
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('127.0.0.1', self.port))
                sock.listen()
                sock.setblocking(False)
                sel = selectors.DefaultSelector()
                sel.register(sock, selectors.EVENT_READ, data=self.handleNewConn)

                while True: 
                    self.cleanCache()
                    events = sel.select(timeout=1)
                    for key, mask in events:
                        callback = key.data
                        callback(sel, key, mask)

                    time.sleep(0.1)
            except Exception as error:
                self.safePrint(error)
                sock.close()
            


