'''
Chopsticks: a sequential task manager for Linux & MacOS

task: define Task class
'''

import os
import signal
import psutil
import subprocess
import time
from state import TaskState

cnt = 0
class Task:
    def __init__(self, cmd: str, cwd: str, out: str) -> None:
        global cnt
        self.idx = cnt
        cnt += 1
        self.cmd = cmd
        self.cwd = cwd
        self.out = out
        self.state = TaskState.waiting
        self.submit_time = time.localtime()
        self.start_time = None
        self.finish_time = None
        self._duration = None
        self.pid = None

    def run(self):
        self.start_time = time.localtime()
        self.state = TaskState.running
        #ret = os.system(f'{self.cmd} > {self.out} 2>&1')
        process = subprocess.Popen(f'{self.cmd} > {self.out} 2>&1', shell=True, cwd=self.cwd)
        self.pid = process.pid
        process.wait()
        self.finish()
        if process.returncode == 0:
            self.state = TaskState.finished
        else:
            self.state = TaskState.crashed

    def cancel(self):
        if self.state == TaskState.running:
            os.kill(self.pid, signal.SIGINT)
            for p in psutil.Process(self.pid).children(recursive=True):
                os.kill(p.pid, signal.SIGINT)
        self.finish()
        self.state = TaskState.cancelled

    def crash(self):
        self.finish()
        self.state = TaskState.crashed

    def finish(self):
        self.finish_time = time.localtime()
        if self.start_time:
            self._duration = time.mktime(self.finish_time) - \
                time.mktime(self.start_time)
            
    def duration(self):
        if self.state == TaskState.running:
            return time.time() - time.mktime(self.start_time)
        return self._duration

    def done(self) -> bool:
        return self.state in [TaskState.finished, TaskState.crashed, TaskState.cancelled]