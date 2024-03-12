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
import json
from config import CMD_FOLDER, RET_FOLDER, RETRY_TIMES, METADATA
from args import parser, pre_parser, submit_parser

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

def trigger(args: dict):
    if not guard_ready():
        if args['sub_command'] == 'quit':
            print('[quit] guard prcoess is not running, no need to quit')
            return
        print('[trigger] start a guard process')
        subprocess.Popen('chopsticks')
        time.sleep(1)

    with open(METADATA, 'r') as f:
        metadata = json.load(f)
    sync_cnt = metadata['sync_cnt']
    with open(METADATA, 'w') as f:
        metadata['sync_cnt'] = sync_cnt + 1
        json.dump(metadata, f)

    args['cwd'] = os.getcwd()
    args['tty'] = subprocess.run(['tty'], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(CMD_FOLDER, f'{sync_cnt}.ret'), 'w') as f:
        json.dump(args, f)
    ret_cnt = None
    get_ret = False
    for _ in range(RETRY_TIMES):
        rets = sorted(os.listdir(RET_FOLDER), key=lambda x: int(x.split('.')[0]))
        for ret_name in rets:
            ret_cnt = int(ret_name.split('.')[0])
            ret_file = os.path.join(RET_FOLDER, ret_name)
            try:
                with open(ret_file, 'r') as f:
                    ret = ''.join(f.readlines())
                os.remove(ret_file)
            except:
                print(f'[trigger] ERROR: failed to load {ret_file}')
                continue
            if ret_cnt == sync_cnt:
                get_ret = True
            elif ret_cnt < sync_cnt and ret_cnt > 0:
                print(f'[trigger] WARNING: find antique responses (sync={ret_cnt})')
            print(ret)  # return messages
            if ret_cnt < sync_cnt and ret_cnt > 0:
                print('[trigger] WARNING: antique responses finished (sync={ret_cnt})')
        if get_ret:
            break
        time.sleep(0.1)
    if not get_ret:
        print(f'[trigger] ERROR: failed to get responses (sync={sync_cnt})')

if __name__ == '__main__':
    pre_args, unkown_args = pre_parser.parse_known_args()
    if pre_args.sub_command == 'submit':
        if len(unkown_args) > 0 and unkown_args[0] in ['-h', '--help']:
            submit_parser.print_help()
        else:
            args = {'sub_command': 'submit', 'cmd': ' '.join(unkown_args)}
            trigger(args)
    else:
        args = vars(parser.parse_args())
        trigger(args)