from trigger import trigger
import sys, os

if __name__ == '__main__':
    if len(sys.argv) > 1:
        trigger('submit', f'{os.getcwd()} {" ".join(sys.argv[1:])}')