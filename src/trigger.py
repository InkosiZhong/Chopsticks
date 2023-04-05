'''
Chopsticks: a sequential task manager for Linux & MacOS

Commands:
> credirect: redirect the output to a terminal or file
> csubmit: submit a new task into the queue
> ccancel: cancel an assigned task
> cls: list all tasks in the waiting list
> cclean: clean all histories
'''
import os
import psutil
import subprocess
import time
from config import CMD_PIPE, RET_PIPE

def guard_ready() -> bool:
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        try:
            if 'chopsticks' in p.name():
                return True
        except:
            pass
    return False

sync_cnt = 0 # sync counter
def trigger(op: str, cmd: str):
    if not guard_ready():
        print('[trigger] start a guard process')
        subprocess.Popen('chopsticks')
        time.sleep(1)
    wf = os.open(CMD_PIPE, os.O_SYNC | os.O_CREAT | os.O_RDWR)
    rf = os.open(RET_PIPE, os.O_RDONLY)
    global sync_cnt
    os.write(wf, f'{sync_cnt} {op} {cmd}'.encode())
    while True:
        s = os.read(rf, 1024)
        if len(s) == 0:
            break
        get_ret = False
        for ret in s.decode().split('sync_cnt='):
            try:
                # is sync_cnt
                ret_cnt = int(ret)
                if ret_cnt is not None:
                    if ret_cnt < sync_cnt:
                        print('[trigger] the above outputs are antique')
                    elif ret_cnt < sync_cnt:
                        print('[trigger] the above outputs are intended')
                    else:
                        get_ret = True
                    continue
            except:
                print(ret)
        if get_ret:
            break
    sync_cnt += 1
    os.close(wf)
    os.close(rf)