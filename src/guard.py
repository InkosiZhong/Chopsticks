'''
Chopsticks: a sequential task manager for Linux & MacOS

guard: this guard class will stay online
'''

import os, shutil
import time
import json
import subprocess
from core import TaskManager
from utils import format_duration
from tabulate import tabulate
from config import CMD_FOLDER, RET_FOLDER, METADATA

class Guard:
    def __init__(self) -> None:
        self.out = '/tmp/out.txt'
        self.manager = None
        self.format = '%m-%d %H:%M:%S'
        self.handlers = {
            'ls': self.ls,
            'submit': self.submit,
            'cancel': self.cancel,
            'restart': self.restart,
            'clean': self.clean,
            'redirect': self.redirect,
            'quit': self.quit
        }

        if os.path.exists(CMD_FOLDER):
            shutil.rmtree(CMD_FOLDER)
        if os.path.exists(RET_FOLDER):
            shutil.rmtree(RET_FOLDER)
        os.makedirs(CMD_FOLDER)
        os.makedirs(RET_FOLDER)
        if os.path.exists(METADATA):
            os.remove(METADATA)
        with open(METADATA, 'w') as f:
            json.dump({'sync_cnt': 0}, f)

        tty = subprocess.run(['tty'], capture_output=True, text=True).stdout.strip()
        self.redirect({'dst': tty}, -1)
        print('[guard] guard process ready')

    def call_back(self, ctx: str, sync_cnt: int):
        if sync_cnt >= 0:
            with open(os.path.join(RET_FOLDER, f'{sync_cnt}.ret'), 'w') as f:
                f.write(ctx)

    def redirect(self, args: dict, sync_cnt: int):
        if args['dst'] is None:
            args['dst'] = args['tty']
        if self.manager is None:
            self.call_back(f'[redirect] set as {args["dst"]}', sync_cnt)
        else:
            self.call_back(f'[redirect] {self.out} -> {args["dst"]}', sync_cnt)
        self.out = args['dst']
        self.manager = TaskManager(self.out)
    
    def submit(self, args: dict, sync_cnt: int):
        idx = self.manager.submit(args['cmd'], args['cwd'])
        self.call_back(f'[submit] id={idx}', sync_cnt)

    def cancel(self, args: dict, sync_cnt: int):
        idx = args['id']
        if self.manager.cancel(idx):
            if idx is None:
                self.call_back(f'[cancel] all waiting tasks are cancelled', sync_cnt)
            else:
                self.call_back(f'[cancel] id={idx}', sync_cnt)
        else:
            if idx is None:
                self.call_back(f'[cancel] ERROR: failed to cancel the tasks', sync_cnt)
            else:
                self.call_back(f'[cancel] ERROR: failed to cancel the task ({idx})', sync_cnt)

    def restart(self, args: dict, sync_cnt: int):
        idx = args['id']
        restart_idx = self.manager.restart(idx)
        if restart_idx != -1:
            self.call_back(f'[restart] id={idx}->{restart_idx}', sync_cnt)
        else:
            self.call_back(f'[restart] ERROR: failed to restart the task ({idx})', sync_cnt)
        
    def format_time(self, t):
        if t is None:
            return 'N/A'
        else:
            return time.strftime(self.format, t)

    def ls(self, args: dict, sync_cnt: int):
        if args['done'] or args['not_done']:
            tasks = self.manager.get_tasks(args['latest_n'], args['done'], args['not_done'])
        else: # no signal
            tasks = self.manager.get_tasks(args['latest_n'])
        if args['long']:
            header = ['id', 'state', 'submit', 'start', 'end', 'duration', 'command']
        else:
            header = ['id', 'state', 'submit', 'command']
        if args['pid']:
            header += ['pid']
        data = [header]
        for task in tasks:
            if args['long']:
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
            if args['pid']:
                record += [task.pid if task.pid else 'N/A']
            data.append(record)
        self.call_back(tabulate(data, headers='firstrow'), sync_cnt)

    def clean(self, args: dict, sync_cnt: int):
        n = self.manager.clean()
        self.call_back(f'[clean] {n} tasks', sync_cnt)

    def quit(self, args: dict, sync_cnt: int) -> bool:
        if args['force']:
            self.cancel({'id': None}, -1)
        elif not self.manager.all_done():
            self.call_back('[quit] tasks are still running, use \'quit -f\' to quit anyway', sync_cnt)
            return False
        self.call_back('[quit] bye', sync_cnt)
        return True
    
    def run(self):
        while True:
            cmds = sorted(os.listdir(CMD_FOLDER), key=lambda x: int(x.split('.')[0]))
            if len(cmds) == 0:
                time.sleep(1e-2)
                continue
            for cmd_name in cmds:
                sync_cnt = int(cmd_name.split('.')[0])
                cmd_file = os.path.join(CMD_FOLDER, cmd_name)
                try:
                    with open(cmd_file, 'r') as f:
                        args = json.load(f)
                    os.remove(cmd_file)
                except:
                    print(f'[chopsticks] ERROR: failed to load {cmd_file}')
                    continue
                op = args['sub_command']
                self.handlers[op](args, sync_cnt)
                if op == 'quit':
                    return

if __name__ == '__main__':
    exec = Guard()
    exec.run()