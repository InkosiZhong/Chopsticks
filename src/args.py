import argparse

# pre parser
pre_parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
subparsers = pre_parser.add_subparsers(dest='sub_command', required=False)
submit_parser = subparsers.add_parser('ls', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('submit', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('cancel', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('restart', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('redirect', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('quit', allow_abbrev=False, add_help=False)
submit_parser = subparsers.add_parser('clean', allow_abbrev=False, add_help=False)

# real parser
parser = argparse.ArgumentParser(description='Chopsticks: a sequential task manager ', allow_abbrev=False)
subparsers = parser.add_subparsers(title='commands', dest='sub_command', required=False)
# ls
ls_parser = subparsers.add_parser('ls', help='list all tasks', description='ls: list all tasks', allow_abbrev=False)
ls_parser.add_argument('-l', '--long', action='store_true', help='show long info')
ls_parser.add_argument('-p', '--pid', action='store_true', help='show PID')
ls_parser.add_argument('-n', '--latest-n', type=int, default=None, help='show the latest n records')
ls_parser.add_argument('--done', action='store_true', help='show the records that are already finished|crashed|cancelled')
ls_parser.add_argument('--not-done', action='store_true', help='show the records that are still running|waiting')
# submit
submit_parser = subparsers.add_parser('submit', help='submit a new task', description='submit: submit a new task', allow_abbrev=False)
submit_parser.add_argument('cmd', type=str, nargs='+', help='command you want to submit')
# cancel
cancel_parser = subparsers.add_parser('cancel', help='cancel a task by ID', description='cancel: cancel a task by ID', allow_abbrev=False)
cancel_parser.add_argument('--id', type=int, required=False, help='task ID you want to cancel')
# restart
restart_parser = subparsers.add_parser('restart', help='restart a task by ID', description='restart: restart a task by ID', allow_abbrev=False)
restart_parser.add_argument('--id', type=int, required=True, help='task ID you want to restart')
# redirect
redirect_parser = subparsers.add_parser('redirect', help='redirect the output', description='redirect: redirect the output', allow_abbrev=False)
redirect_parser.add_argument('--dst', type=str, required=False, help='redirect destination')
# quit
quit_parser = subparsers.add_parser('quit', help='quit the guard process', description='cquit: quit the guard process', allow_abbrev=False)
quit_parser.add_argument('-f', '--force', action='store_true', help='quit anyway, ignoring the running|waiting tasks')
# clean
clean_parser = subparsers.add_parser('clean', help='clean all finished tasks', description='clean: clean all finished tasks', allow_abbrev=False)