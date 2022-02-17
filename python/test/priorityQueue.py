# Author: Joonseo Park

class SimplePriorityQueue( object ):
    '''
        Simple priority queue class
        stream out only priority items found in user defined priority keys
    '''
    PRIORITY_KEYS = [0, 10]
    def __init__(self):
        self._queue = []

    def __repr__(self):
        return '( "%s" )' % ( self.__class__.__name__ )

    def __str__(self):
        return " ".join(["%s"%stream for stream in self.queue])
    
    @property
    def queue(self):
        return self._queue

    @property
    def size(self):
        return len(self.queue)

    def is_empty(self):
        return self.size == 0

    def add(self, data):
        self.queue.append(data)

    # delete queues if its key is not in PRIORITY_KEYS
    def set(self):
        try:
            i = 0
            for i in range(len(self._queue)):
                if not self.queue[i].keys()[0] in self.PRIORITY_KEYS:
                    del self._queue[i]
        except IndexError:
            pass



if __name__ == "__main__":
    streams = [
        {0: "Jenny"},
        {20: "Tom"},
        {10: "John"},
        {5: "Brad"},
        {0: "Joonseo"},
        {13: "Tommny"}
    ]
    myQueue = SimplePriorityQueue()
    for stream in streams:
        myQueue.add(stream)
    print(myQueue)
    myQueue.set()

    print(myQueue)