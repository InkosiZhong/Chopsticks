'''
Chopsticks: a sequential task manager for Linux & MacOS

state: define all possible states for a task
'''

from enum import Enum, unique

@unique
class TaskState(Enum):
    finished = 0
    running = 1
    waiting = 2
    cancelled = 3
    crashed = 4