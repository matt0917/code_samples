class SimplePriorityQueue( object ):
    '''
        Simple priority queue class
        stream out only priority items found in user defined priority keys
    '''
    PRIORITY_KEY = [0, 10]
    def __init__(self):
        '''
        construtor
        '''
        self.queue = []
  
    def __repr__(self):
        return '( "%s" )' % ( self.__class__.__name__ )

    def __str__(self):
        return ' '.join(["%s"%i for i in self.queue])
  
    @property
    def size(self):
        return len(self.queue)

    def is_empty(self):
        return (self.size == 0)

    # add queue
    def add(self, data):
        self.queue.append(data)
  
    # return removed item based on the key's priority
    def remove(self):
        try:
            item = None
            idx = 0
            for i in range(len(self.queue)):
                key = list(self.queue[i].keys())[0]
                if key in self.PRIORITY_KEY:
                    idx = i
                    break
            item = self.queue[idx]
            del self.queue[idx]
            return item
        except IndexError as e:
            print(e)
            exit()




if __name__ == '__main__':
    streams = [
        {0: "Jenny_cmd"},
        {20: "Tom_cmd"},
        {10: "John_cmd"},
        {5: "Brad_cmd"},
        {0: "Joonseo_cmd"},
        {13: "Tommny_cmd"}
    ]
    myQueue = SimplePriorityQueue()
    for stream in streams:
        myQueue.add(stream)
    # dequeue in the priority order
    results = []
    while not myQueue.is_empty():
        results.append(myQueue.remove())
    print(results)