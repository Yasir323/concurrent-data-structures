from abc import ABC
import functools
from collections import deque
import threading
import time
from typing import Optional

from concurrent_collections import (
    BlockingQueue,
    T,
    RealNumber,
    Empty,
    Full
)


class SynchronousQueue(BlockingQueue, ABC):

    def __init__(self):
        self._mutex = threading.Lock()
        self._not_empty = threading.Condition(self._mutex)
        self._not_full = threading.Condition(self._mutex)
        self._max_size = 1
        self._queue = deque([], maxlen=self._max_size)

    def put(self, item: T, block: bool = True, timeout: Optional[RealNumber] = None) -> None:
        if item is None:
            raise ValueError("item is None")
        with self._not_full:
            if not block:
                if self._qsize() >= self._max_size:
                    raise Full
            elif timeout is None:
                while self._qsize() >= self._max_size:
                    self._not_full.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be non-negative")
            else:
                end_time = time.time() + timeout
                while self._qsize() >= self._max_size:
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        raise Full
                    self._not_full.wait(remaining)
            self._push(item)
            self._not_empty.notify()

    @functools.singledispatchmethod
    def put(self, item: T) -> None:
        return self.put(item, block=False)

    def get(self, block=True, timeout=None):
        with self._not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    # Wait indefinitely for some thread to notify
                    # queue is not empty anymore
                    self._not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be non-negative")
            else:
                end_time = time.time() + timeout
                while not self._qsize():
                    remaining = end_time - time.time()
                    if remaining <= 0:
                        raise Empty
                    # Wait for timeout seconds for some thread to
                    # notify that queue is not empty anymore
                    self._not_empty.wait(timeout)
            item = self._pop()
            # Notify waiting threads that queue is not full anymore
            self._not_full.notify()
            return item

    @functools.singledispatchmethod
    def get(self):
        return self.get(block=False)

    def peek(self) -> Optional[T]:
        if self._qsize():
            return self._queue[-1]
        return None

    def is_empty(self) -> bool:
        with self._mutex:
            return not self._qsize()

    def is_full(self) -> bool:
        with self._mutex:
            return 0 < self._max_size <= self._qsize()

    def _pop(self) -> T:
        return self._queue.popleft()

    def _push(self, item: T):
        self._queue.append(item)

    def _qsize(self) -> int:
        return len(self._queue)
