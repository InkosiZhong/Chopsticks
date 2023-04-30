import argparse

# ls
ls_parser = argparse.ArgumentParser(description='cls: list all files', allow_abbrev=False)
ls_parser.add_argument('-l', '--long', action='store_true', help='show long info')
ls_parser.add_argument('-p', '--pid', action='store_true', help='show PID')
ls_parser.add_argument('-n', '--latest-n', type=int, default=None, help='show the latest n records')
ls_parser.add_argument('--done', action='store_true', help='show the records that are already finished|crashed|cancelled')
ls_parser.add_argument('--not-done', action='store_true', help='show the records that are still running|waiting')

# quit
quit_parser = argparse.ArgumentParser(description='cquit: quit the guard process', allow_abbrev=False)
quit_parser.add_argument('-f', '--force', action='store_true', help='quit anyway, ignoring the running|waiting tasks')