import time


def is_even1(value):
    """
    + Лучше для понимания
    """
    return value % 2 == 0


def is_even2(value):
    """
    + Побитовые операции выполняются быстрее
    """
    return value & 1 == 0


def measure_time(is_even):
    t = time.time()
    for i in range(1000000):
        is_even(i)
    return time.time() - t


print(measure_time(is_even1))
print(measure_time(is_even2))
