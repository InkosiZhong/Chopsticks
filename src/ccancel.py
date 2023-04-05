from trigger import trigger
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        trigger('cancel', ' '.join(sys.argv[1:]))
    else:
        trigger('cancel', '')