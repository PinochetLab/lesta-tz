import time
from collections import deque


class CircularFifoBuffer:
    def size(self): ...
    def is_empty(self): ...
    def is_full(self): ...
    def push(self, item): ...
    def pop(self): ...
    def clear(self): ...


class CircularFifoBufferArray(CircularFifoBuffer):
    def __init__(self, capacity):
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._size = 0
        self._head = 0
        self._tail = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == self._capacity

    def _move(self, index):
        index += 1
        index %= self._capacity
        return index

    def push(self, item):
        self._buffer[self._head] = item
        self._head = self._move(self._head)
        if self.is_full():
            self._tail = self._head
        else:
            self._size += 1

    def pop(self):
        if self.is_empty():
            raise Exception('Buffer is empty!')
        value = self._buffer[self._tail]
        self._tail = self._move(self._tail)
        self._size -= 1
        return value

    def clear(self):
        self._size = 0
        self._head = 0
        self._tail = 0


class CircularFifoBufferDeque(CircularFifoBuffer):
    def __init__(self, capacity):
        self._capacity = capacity
        self._buffer = deque([], maxlen=capacity)

    def size(self):
        return len(self._buffer)

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == self._capacity

    def push(self, item):
        if self.is_full():
            self._buffer.popleft()
        self._buffer.append(item)

    def pop(self):
        if self.is_empty():
            raise Exception('Buffer is empty!')
        return self._buffer.popleft()

    def clear(self):
        self._buffer.clear()


class CircularFifoBufferList(CircularFifoBuffer):
    class Node:
        def __init__(self):
            self.right = None
            self.value = None

    def __init__(self, capacity):
        self._capacity = capacity
        nodes = [self.Node() for _ in range(capacity)]
        for i in range(capacity - 1):
            nodes[i].right = nodes[i + 1]
        nodes[capacity - 1].right = nodes[0]
        self._tail = self._head = nodes[0]
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == self._capacity

    def push(self, item):
        self._head.value = item
        self._head = self._head.right
        if self.is_full():
            self._tail = self._head
        else:
            self._size += 1

    def pop(self):
        if self.is_empty():
            raise Exception('Buffer is empty!')
        value = self._tail.value
        self._tail = self._tail.right
        self._size -= 1
        return value

    def clear(self):
        self._head = self._tail
        self._size = 0


def test_circular_fifo_buffer_list(circular_fifo_buffer_class):
    cb = circular_fifo_buffer_class(3)
    cb.push(1)
    assert cb.size() == 1
    assert cb.pop() == 1
    cb.push(1)
    cb.push(2)
    cb.push(3)
    assert cb.is_full()
    assert cb.pop() == 1
    cb.push(4)
    cb.push(5)
    assert cb.pop() == 3


def check_time(circular_fifo_buffer_class):
    cb = circular_fifo_buffer_class(1000)
    t = time.time()
    for i in range(100000):
        if i % 3 == 2:
            cb.pop()
        else:
            cb.push(i)
    return time.time() - t


test_circular_fifo_buffer_list(CircularFifoBufferArray)
test_circular_fifo_buffer_list(CircularFifoBufferDeque)
test_circular_fifo_buffer_list(CircularFifoBufferList)

print(check_time(CircularFifoBufferArray))
print(check_time(CircularFifoBufferDeque))
print(check_time(CircularFifoBufferList))

"""
Реализация циклического буфера на односвязном списке оказалась быстрее реализации
на массиве. Deque реализована через двусвязный список.
Обе реализации имеют асимптотику всех методов O(1).
Я думаю, что в реализации с массивом константа, отвечающая за сдвиг, больше чем в
реализации с односвязным списком. 
"""
