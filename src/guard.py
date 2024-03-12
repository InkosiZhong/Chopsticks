'''
Chopsticks: a sequential task manager for Linux & MacOS

guard: this guard class will stay online
'''

import os
import time
from typing import Sequence
from core import TaskManager
from utils import format_duration
from tabulate import tabulate
from config import CMD_PIPE, RET_PIPE, SYNC_SIGN
from args import ls_parser, quit_parser

class Guard:
    def __init__(self) -> None:
        self.out = '/tmp/out.txt'
        self.manager = None
        self.format = '%m-%d %H:%M:%S'

        if os.path.exists(CMD_PIPE):
            os.remove(CMD_PIPE)
        if os.path.exists(RET_PIPE):
            os.remove(RET_PIPE)
        os.mkfifo(CMD_PIPE)
        os.mkfifo(RET_PIPE)
        self.wf = os.open(RET_PIPE, os.O_SYNC | os.O_CREAT | os.O_RDWR)
        tmp = os.open(CMD_PIPE, os.O_SYNC | os.O_CREAT | os.O_RDWR)
        self.rf = os.open(CMD_PIPE, os.O_RDONLY)
        os.close(tmp)

        self.redirect(self.out, -1)
        print('[guard] guard process ready')

    def call_back(self, ctx: str, sync_cnt: int):
        if sync_cnt >= 0:
            os.write(self.wf, ctx.encode())
            os.write(self.wf, f'{SYNC_SIGN}{sync_cnt}'.encode())

    def redirect(self, out: str, sync_cnt: int):
        if self.manager is None:
            self.call_back(f'[redirect] set as {out}', sync_cnt)
        else:
            self.call_back(f'[redirect] {self.out} -> {out}', sync_cnt)
        self.out = out
        self.manager = TaskManager(self.out)
    
    def submit(self, cmd: str, cwd: str, sync_cnt: int):
        idx = self.manager.submit(cmd, cwd)
        self.call_back(f'[submit] id={idx}', sync_cnt)

    def cancel(self, idx: int, sync_cnt: int):
        if self.manager.cancel(idx):
            if idx is None:
                self.call_back(f'[cancel] all waiting tasks are cancelled', sync_cnt)
            else:
                self.call_back(f'[cancel] id={idx}', sync_cnt)
        else:
            if idx is None:
                self.call_back(f'[error] failed to cancel the tasks', sync_cnt)
            else:
                self.call_back(f'[error] failed to cancel the task ({idx})', sync_cnt)

    def restart(self, idx: int, sync_cnt: int):
        restart_idx = self.manager.restart(idx)
        if restart_idx != -1:
            self.call_back(f'[restart] id={idx}->{restart_idx}', sync_cnt)
        else:
            self.call_back(f'[error] failed to restart the task ({idx})', sync_cnt)
        
    def format_time(self, t):
        if t is None:
            return 'N/A'
        else:
            return time.strftime(self.format, t)

    def ls(self, param: Sequence[str], sync_cnt: int):
        args = ls_parser.parse_args(param)
        if args.done or args.not_done:
            tasks = self.manager.get_tasks(args.latest_n, args.done, args.not_done)
        else: # no signal
            tasks = self.manager.get_tasks(args.latest_n)
        if args.long:
            header = ['id', 'state', 'submit', 'start', 'end', 'duration', 'command']
        else:
            header = ['id', 'state', 'submit', 'command']
        if args.pid:
            header += ['pid']
        data = [header]
        for task in tasks:
            if args.long:
                record = [
                    task.idx,
                    task.state.name,
                    self.format_time(task.submit_time),
                    self.format_time(task.start_time),
                    self.format_time(task.finish_time),
                    format_duration(task.duration()),
                    task.cmd
                ]
            else:
                record = [
                    task.idx,
                    task.state.name,
                    self.format_time(task.submit_time),
                    f'{task.cmd[:47]}...'
                ]
            if args.pid:
                record += [task.pid if task.pid else 'N/A']
            data.append(record)
        self.call_back(tabulate(data, headers='firstrow'), sync_cnt)

    def clean(self, sync_cnt: int):
        n = self.manager.clean()
        self.call_back(f'[clean] {n} tasks', sync_cnt)

    def quit(self, param: Sequence[str], sync_cnt: int) -> bool:
        args = quit_parser.parse_args(param)
        if args.force:
            self.cancel(None, -1)
        elif not self.manager.all_done():
            self.call_back('[quit] tasks are still running, use \'quit force\' to quit anyway', sync_cnt)
            return False
        self.call_back('[quit] bye', sync_cnt)
        return True
                
    def run(self):
        while True:
            s = os.read(self.rf, 1024)
            if len(s) == 0:
                time.sleep(1e-2)
                continue
            ret = s.decode()
            ret = ret.split(' ', 2)
            sync_cnt = int(ret[0])
            op = ret[1]
            if len(ret) == 3:
                param = [x for x in ret[2].split(' ') if x] # not ''
            else:
                param = []
            if op == 'ls':
                self.ls(param, sync_cnt)
            elif op == 'submit':
                try:
                    cwd, cmd = ret[2].split(' ', 1)
                    self.submit(cmd, cwd, sync_cnt)
                except:
                    self.call_back('[error] usage: submit command arg1 arg2 ...', sync_cnt)
            elif op == 'cancel':
                try:
                    idx = int(ret[2])
                except:
                    idx = None
                self.cancel(idx, sync_cnt)
            elif op == 'restart':
                try:
                    idx = int(ret[2])
                    self.restart(idx, sync_cnt)
                except:
                    self.call_back('[error] usage: restart id', sync_cnt)
            elif op == 'clean':
                self.clean(sync_cnt)
            elif op == 'redirect':
                try:
                    self.redirect(ret[2], sync_cnt)
                except:
                    self.call_back('[error] usage: redirect path|terminal', sync_cnt)
            elif op == 'quit':
                if self.quit(param, sync_cnt):
                    break
        os.close(self.rf)
        os.close(self.wf)

if __name__ == '__main__':
    exec = Guard()
    exec.run()