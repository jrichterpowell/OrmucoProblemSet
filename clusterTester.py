import socket,time, random
from cacheNode import Node
from client import CacheClient
from threading import Thread

clusterNames = ['jupiter', 'juno', 'neptune', 'saturn', 'venus', 'pluto', 'vulcan', 'ceres', 'apollo', 'minerva', 'diana', 'mars', 'mercury', 'bacchus', 'proserpine', 'cupid', 'terra', 'somnus', 'ops', 'uranus', 'victoria', 'aurora', 'faunus', 'luna', 'sol', 'hercules', 'ulysses']

ports  = [i for i in range(6555,6575)]

nodes = [Node(5,clusterNames[i], ports[i], position=(random.randint(-10,10), random.randint(-10,10))) for i in range(20)]
if __name__ == "__main__":
    c = CacheClient(nodes=[node.port for node in nodes])

    threads = [Thread(target = node.serve, args = ()) for node in nodes]
    for thread in threads:
        thread.start() 

    time.sleep(2)
    c.getDistances()
    time.sleep(7)
    c.writeCache('dolphin', '30')
    dol = c.readCache('dolphin')

    print("Dolphin is: ", dol)

    c.getDistances()

