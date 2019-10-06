import socket,time, random
from cacheNode import Node
from client import CacheClient
from threading import Thread, Lock

clusterNames = ['jupiter', 'juno', 'neptune', 'saturn', 'venus', 'pluto', 'vulcan', 'ceres', 'apollo', 'minerva', 'diana', 'mars', 'mercury', 'bacchus', 'proserpine', 'cupid', 'terra', 'somnus', 'ops', 'uranus', 'victoria', 'aurora', 'faunus', 'luna', 'sol', 'hercules', 'ulysses']

ports  = [i for i in range(6555,6563)]
printlock = Lock()
nodes = [Node(5,clusterNames[i], ports[i], position=(random.randint(-10,10), random.randint(-10,10)), lock=printlock) for i in range(len(ports))]


if __name__ == "__main__":
    c = CacheClient(nodes=[node.port for node in nodes])

    threads = [Thread(target = node.serve, args = ()) for node in nodes]
    for thread in threads:
        thread.start() 

    time.sleep(2)
    c.getDistances()
    time.sleep(7)
    json = '{"a": 123, "b": 75}'
    c.writeCache('dolphin', json)

    json = "{'a': 1729, 'b': 540}"
    c.writeCache('cow', json)

    json = "{'a': '-1^\\frac{1}{2}', 'b': 'e'}"
    c.writeCache('elephant', json)

    json = "{'a': 1, 'b': 'apple', 'c': 'triangle'}"
    c.writeCache('dog', json)

    json = "{'a': 1337}"
    c.writeCache('cat', json)

    dol = c.readCache('dolphin')
    print("Value of dolphin is ", dol)

    #should result in cow,do being removed in the cache we just read from, but dolphin from the others
    json = "{'a': 0101010101}"
    c.writeCache('tiger', json)

    #will result in getting elephant bumped out from the cache we read dolphin from, but cow from the others
    json = "{'one': 'Beware the ides of March.', 'two', 'A soothsayer bids you beware the ides of March.' }"
    c.writeCache('emu', json)

