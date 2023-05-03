import functools
import time
from collections import deque
from queue import Full, Empty
import threading
from abc import ABC
from typing import Any

from consurrent_collections import BlockingQueue


class SynchronousQueue(BlockingQueue, ABC):

    def __init__(self):
        self._mutex = threading.Lock()
        self._not_empty = threading.Condition(self._mutex)
        self._not_full = threading.Condition(self._mutex)
        self._max_size = 1
        self._queue = deque([], maxlen=self._max_size)

    def put(self, item: Any) -> None:
        """
        Blocking\n
        Adds the specified element to this queue, waiting if necessary for another thread to receive it.

        :param item: Value to be inserted

        :raises ValueError: if item is None
        """
        if item is None:
            raise ValueError("item is None")
        with self._not_full:
            # To guard against spurious wake-ups we put
            # wait() inside a while loop
            while len(self._queue) == self._max_size:
                # Wait until some thread notifies
                # that queue has space to accommodate
                # the item
                self._not_full.wait()
            self._queue.append(item)
            self._not_empty.notify()

    def offer(self, item: Any, block=True, timeout=None) -> bool:
        if item is None:
            raise ValueError("item is None")
        with self._not_full:
            if not block:
                if len(self._queue) >= self._max_size:
                    return False
            elif timeout is None:
                while len(self._queue) >= self._max_size:
                    self._not_full.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be non-negative")
            else:
                endtime = time.time() + timeout
                while len(self._queue) >= self._max_size:
                    remaining = endtime - time.time()
                    if remaining <= 0:
                        return False
                    self._not_full.wait(remaining)
            self._queue.append(item)
            self._not_empty.notify()
        return True

    @functools.singledispatchmethod
    def offer(self, item: Any) -> bool:
        """
        Non-Blocking\n
        Inserts the specified element into this queue, waiting if necessary up to the specified wait time for
        another thread to receive it.

        :param item: Value to be inserted

        :raises ValueError: if item is None

        :return: True if successful otherwise False
        """
        return self.offer(item, block=False)
