import sys

def numberReader():
    while True:
        try:
            buf = sys.stdin.read(1)
            num = int(buf)
            print(num)
            return
        except EOFError:
            print("EOFError", file=sys.stderr)
            return
        except ValueError:
            print("ValueError", file=sys.stderr)
            continue
        except KeyboardInterrupt:
            print("KeyboardInterrupt", file=sys.stderr)
            return

numberReader()
