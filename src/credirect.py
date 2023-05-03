from trigger import trigger
import sys
import subprocess

if __name__ == '__main__':
    if len(sys.argv) > 1:
        out = sys.argv[1]
        trigger('redirect', out)
    else: # redirect here
        result = subprocess.run(['tty'], capture_output=True, text=True)
        trigger('redirect', result.stdout.strip())