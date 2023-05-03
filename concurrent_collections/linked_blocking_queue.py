class LinkedBlockingQueue:
    def __init__(self, maxsize=0):
        self.queue = Queue(maxsize)
        self.condition = Condition()

    def put(self, item, block=True, timeout=None):
        with self.condition:
            if block:
                while self.queue.full():
                    self.condition.wait(timeout)
            self.queue.put(item)
            self.condition.notify()

    def get(self, block=True, timeout=None):
        with self.condition:
            if block:
                while self.queue.empty():
                    self.condition.wait(timeout)
            item = self.queue.get()
            self.condition.notify()
            return item
