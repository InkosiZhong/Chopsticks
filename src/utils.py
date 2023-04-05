from typing import Any, Callable, Tuple
from task import Task

def binary_search(arr_like: list, x: Any, hit_func: Callable[[Any, Any], int]=lambda x, y: x-y) -> int:
    def _search(l: int, r: int):
        if r <= l:
            return None
        mid = (l + r) // 2
        hit = hit_func(x, arr_like[mid])
        if hit == 0:
            return mid
        elif hit > 0:
            return _search(mid + 1, r)
        else:
            return _search(l, mid)
    return _search(0, len(arr_like))

def hit_task(x: int, y: Tuple[Task, Any]) -> int:
    if x < y[0].idx:
        return -1
    elif x > y[0].idx:
        return 1
    else:
        return 0

if __name__ == '__main__':
    tasks = [(Task('', ''), None) for _ in range(10)]
    for i in range(10):
        print(binary_search(tasks, i, hit_task))