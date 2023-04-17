from trigger import trigger
from args import quit_parser
import os, sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # pre-parsing
        param = sys.argv[1:]
        if '-h' in param or '--help' in param:
            print(f'[quit] {quit_parser.format_help()}')
            os._exit(0)
        try:
            args = quit_parser.parse_args(param)
        except:
            print(f'[quit] {quit_parser.format_help()}')
            os._exit(0)
        trigger('quit', ' '.join(param))
    else:
        trigger('quit', '')