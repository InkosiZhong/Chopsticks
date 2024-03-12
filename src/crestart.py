from trigger import trigger
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        trigger('restart', ' '.join(sys.argv[1:]))
    else:
        trigger('restart', '')