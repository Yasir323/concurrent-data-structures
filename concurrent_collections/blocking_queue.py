from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Optional, Union, TypeVar

RealNumber = Union[float, int]
T = TypeVar('T')


class Empty(Exception):
    pass


class Full(Exception):
    pass


class BlockingQueue(ABC):

    @abstractmethod
    def put(self, item: T, block: bool = True, timeout: Optional[RealNumber] = None) -> None:
        """
        Blocking (Optional)\n
        Inserts the specified element into this queue, waiting up to the specified wait time if necessary for space
        to become available.

        :param item: Value to be inserted
        :param block: If set to True, blocks for the specified time
        :param timeout: Specified timeout

        :raises ValueError: If item is None
        :raises Full: If queue is full
        """
        pass

    @abstractmethod
    @singledispatchmethod
    def put(self, item: T) -> None:
        """
        Non-Blocking\n
        Inserts the specified element into this queue if it is possible to do so immediately without violating capacity
        restrictions. If no space is currently available, raises Empty.

        :param item: Value to be inserted

        :raises ValueError: If item is None
        :raises Full: If queue is full
        """
        pass

    @abstractmethod
    def get(self, block: bool = True, timeout: Optional[RealNumber] = None):
        """
        Blocking (Optional)\n
        Retrieves and removes the head of this queue, waiting up to the specified wait time if necessary for an
        element to become available.

        :param block: If set to True, blocks for the specified time
        :param timeout: Specified timeout

        :raises Empty: If queue is empty

        :return: Item at the head of the queue
        """
        pass

    @abstractmethod
    @singledispatchmethod
    def get(self) -> T:
        """
        Non-Blocking\n
        Retrieves and removes the head of this queue, or returns null if this queue is empty.

        :raises Empty: If queue is empty

        :return: the head of the queue, if any
        """

    @abstractmethod
    def peek(self) -> Optional[T]:
        """
        Non-Blocking\n
        Retrieves, but does not remove, the head of this queue, or returns None if this queue is empty.

        :return: the head of the queue, or None if this queue is empty
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Non-Blocking\n
        Return True if the queue is empty, False otherwise (not reliable!).

        :return: True if queue is empty, else False
        """
        pass

    def is_full(self) -> bool:
        """
        Non-Blocking\n
        Return True if the queue is full, False otherwise (not reliable!).

        :return: True if the queue is full, False otherwise
        """
        pass
