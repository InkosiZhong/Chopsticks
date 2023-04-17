'''
Chopsticks: a sequential task manager for Linux & MacOS

core: this class actually manage the tasks
'''

from typing import List, Tuple
from state import TaskState
from task import Task
from utils import binary_search, hit_task
from concurrent.futures import ThreadPoolExecutor, Future
from copy import copy

class TaskManager:
    def __init__(self, out: str='out.txt') -> None:
        self.out = out
        self.task_queue: List[Tuple[Task, Future]] = []
        self.pool = ThreadPoolExecutor(1) # sequential worker

    def redirect(self, out: str):
        """redirect the output to a file or terminal

        Args:
            out (str): the path of a file or terminal
        """
        self.out = out
        for i in range(len(self.task_queue)):
            if self.task_queue[i][0].state is TaskState.waiting:
                self.task_queue[i][0].out = self.out

    def submit(self, cmd: str, cwd: str) -> int:
        """submit a new task

        Args:
            cmd (str): user provided command
            cwd (str): the execution path

        Returns:
            int: index of the submitted task
        """
        task = Task(cmd, cwd, self.out)
        ret = self.pool.submit(task.run)
        self.task_queue.append((task, ret))
        return task.idx

    def get_tasks(self, n: int=None, done: bool=True, not_done: bool=True) -> List[Task]:
        """get submitted tasks and their states

        Args:
            n (int): return the nearest n-th tasks, None for all
            done (bool): return the tasks in [finished|crashed|cancelled] states
            not_done (bool): return the tasks in [running|waiting] states

        Returns:
            List[Task]: all tasks in the history and
        """
        def is_valid(task):
            nonlocal done, not_done
            if done and not_done: # valid anyway
                return True
            task_done = task.done()
            return (done and task_done) or (not_done and not task_done)
        tasks = [copy(task) for task, _ in self.task_queue if is_valid(task)]
        if n is not None:
            n = min(len(tasks), n)
            tasks = tasks[-n:]
        return tasks

    def cancel(self, idx: int=None) -> bool:
        """cancel specified tasks

        Args:
            idx (int, optional): cancel the task with the given id, 
            set None to cancal all tasks in the waiting list. Defaults to None.

        Returns:
            bool: if successfully cancelled
        """
        if idx is None:
            cancel_any = False
            for i in range(-len(self.task_queue)+1, 0): # from the tail
                task, future = self.task_queue[-i]
                if task.state == TaskState.waiting:
                    cancelled = future.cancel() # TODO: cannot cancel the current running task
                    if cancelled:
                        cancel_any = True
                        task.cancel()
            return cancel_any
        else:
            i = binary_search(self.task_queue, idx, hit_task)
            if i is None:
                return False
            task, future = self.task_queue[i]
            cancelled = future.cancel()
            if not cancelled:
                return False
            task.cancel()
            return True

    def clean(self) -> int:
        """clean all history tasks

        Returns:
            int: number of the cleaned histories
        """
        cnt = 0
        while len(self.task_queue) > 0:
            task, _ = self.task_queue[0]
            if task.state not in [TaskState.waiting, TaskState.running]:
                self.task_queue.pop(0)
                cnt += 1
            else:
                break
        return cnt
    
    def all_done(self) -> bool:
        """all submitted tasks finished

        Returns:
            bool: all done or not
        """
        return all(
            task.state not in [
                TaskState.running, TaskState.waiting
            ] for task, _ in self.task_queue
        )