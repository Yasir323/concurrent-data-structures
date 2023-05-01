from abc import ABC, abstractmethod
from functools import singledispatchmethod
from queue import Queue
from threading import Condition
from typing import Any, Optional


class QueueUnderFlowError(Exception):
    pass


class BlockingQueue(ABC):

    @abstractmethod
    def add(self, item: Any) -> bool:
        """
        Inserts the specified element into this queue if it is possible to do so immediately without violating capacity
        restrictions, returning true upon success and throwing an IllegalStateException if no space is currently
        available. When using a capacity-restricted queue, it is generally preferable to use offer.

        :param item: Value to be inserted

        :raises OverflowError: if the element cannot be added at this time due to capacity restrictions

        :return: True if successful otherwise False
        """
        pass

    @abstractmethod
    def offer(self, item: Any) -> bool:
        """
        Inserts the specified element into this queue if it is possible to do so immediately without violating capacity
        restrictions, returning true upon success and false if no space is currently available. When using a
        capacity-restricted queue, this method is generally preferable to add(E), which can fail to insert an element
        only by throwing an exception.

        :param item: Value to be inserted

        :return: True if successful otherwise False
        """
        pass

    @abstractmethod
    def put(self, item: Any) -> None:
        """
        Inserts the specified element into this queue, waiting if necessary for space to become available.

        :param item: Value to be inserted

        :raises InterruptedError: if Interrupted while waiting
        """
        pass

    @abstractmethod
    @singledispatchmethod
    def offer(self, item: Any, block=True, timeout=None) -> bool:
        """
        Inserts the specified element into this queue, waiting up to the specified wait time if necessary for space
        to become available.

        :param item: Value to be inserted
        :param block: If set to True, blocks for the specified time
        :param timeout: Specified timeout

        :raises InterruptedError: if Interrupted while waiting

        :return: True is successful, otherwise False
        """
        pass

    @abstractmethod
    def remove(self) -> Any:
        """
        Retrieves and removes the head of this queue. This method differs from poll() only in that it throws an
        exception if this queue is empty.

        :raises QueueUnderFlowError: if queue is empty

        :return: the head of the queue
        """

    @abstractmethod
    def poll(self) -> Optional[Any]:
        """
        Retrieves and removes the head of this queue, or returns null if this queue is empty.

        :return: the head of the queue, if any. Otherwise, returns None.
        """

    @abstractmethod
    def take(self) -> Any:
        """
        Retrieves and removes the head of this queue, waiting if necessary until an element becomes available.

        :raises InterruptedError: if interrupted while waiting

        :return: the head of the queue
        """
        pass

    @abstractmethod
    @singledispatchmethod
    def poll(self, block=True, timeout=None):
        """
        Retrieves and removes the head of this queue, waiting up to the specified wait time if necessary for an
        element to become available.

        :param block: If set to True, blocks for the specified time
        :param timeout: Specified timeout

        :return:
        """
        pass

    @abstractmethod
    def element(self) -> Any:
        """
        Retrieves, but does not remove, the head of this queue. This method differs from peek only in that it throws
        an exception if this queue is empty.

        :raises QueueUnderFlowError: if queue is empty

        :return: the head of the queue
        """
        pass

    @abstractmethod
    def peek(self) -> Optional[Any]:
        """
        Retrieves, but does not remove, the head of this queue, or returns null if this queue is empty.

        :return: the head of the queue, or null if this queue is empty
        """
        pass


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
