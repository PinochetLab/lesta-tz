import copy
import random
import sys


def quicksort(array):
    """
    Quicksort является одним из самых быстрых алгоритмов сортировки.
    Среднее время его работы - O(n log n)
    Если важно добиться большой скорости для отсортированных заранее массивов,
    можно установить middle = left, в таком случае для отсортированных массивов
    количество вызовов будет минимальным.
    """
    def _quicksort(lst, left, right):
        if right - left <= 1:
            return

        middle = (left + right - 1) // 2
        target = lst[middle]

        i = left
        j = right - 1

        while True:
            while lst[i] < target:
                i += 1
            while lst[j] > target:
                j -= 1
            if i >= j:
                break
            lst[i], lst[j] = lst[j], lst[i]
            i += 1
            j -= 1

        _quicksort(lst, left, j + 1)
        _quicksort(lst, j + 1, right)
    return _quicksort(array, 0, len(array))


sys.setrecursionlimit(10000)
arr = list(range(100))
sh = copy.deepcopy(arr)
random.shuffle(sh)
quicksort(sh)
assert sh == arr
