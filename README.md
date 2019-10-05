
# Explanation for Q3

## Overview
The solution to this problem is composed of 2 parts 
1. The cache nodes
2. The client node(s)

The cache nodes essentially run a very simple server, which accepts requests from the clients in a simple message protocol, then services them if they are valid. 

The client node is in theory our car or mobile device which is requesting the data from the network.

The main idea is to use the cache nodes as minature data stores, which in practice would store the cache in memory and thus be able to serve requests extremely quickly. 

## Data Consistency
To tackle data consistency, I opted to make the protocol write-to-all. I.e. when a write is requested by the client, the write is sent to all nodes. If the cache is full, by nature of a LRU design, each will dump the least recently used block in that node. 

Reading, however, only updates the LRU status of the block that is actually read. I.e. if the client requests key 'dog' from node A first (we'll explain the ordering briefly), but node A doesn't have an entry with that key, then nothing happens to the contents of node A. Say the client goes on to query node B, which does have an entry with the key 'dog'. Then node B will return the entry, and update the most recently used block to be 'dog'.

This might seem like it would introduce data inconsistency across nodes, but note that since writes are write-all, we can guarantee that all caches have the same value for the same key. They just might not all contain the same key. 

So why didn't I just make it read-all as well? I would argue this implementation is actually much more efficient in a typical edge computing use case. Consider that if we were to implement a cache in every cell-tower or micro-datacenter, then there is a good chance of the client being connected to a large set of cache nodes. By using read-one instead of read-any, we increase the chance that the selected key is found in at least one (but maybe not the closest) cache node. 

Assuming that these nodes are within reasonable proximity to the client — which again I think is likely given the use case imagined above — then the increased chance of finding the key in a cache node, even if it's not the closest node, would provide a sizeable performance improvement.

##  Flexibility
Due to time constraints, this demonstration is obviously not very robust. But by encoding data in a json string and then storing that in the cache, we can provide a high degree of flexibility without seriously increasing complexity (my other idea was to run an in-memory sql database for each node, which would probably work a lot better but is a lot more complicated to implement).

## Expiry 
Each cache node has a time to live paramater which sets the max life (in minutes) of any entry in the cache. A cleanup function is then called every server loop to ensure that the stale entries are deleted. 

