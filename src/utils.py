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

def format_duration(t: int) -> str:
    if t is not None:
        s, t = t % 60, t // 60
        m, t = t % 60, t // 60
        h, d = t % 24, t // 24
        return f'{int(d)} days {int(h):02d}:{int(m):02d}:{int(s):02d}'
    else:
        return 'N/A'

if __name__ == '__main__':
    tasks = [(Task('', ''), None) for _ in range(10)]
    for i in range(10):
        print(binary_search(tasks, i, hit_task))