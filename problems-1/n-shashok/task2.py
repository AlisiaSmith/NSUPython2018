import math
import sys


def is_prime(n):
    for x in range(2, int(math.sqrt(n) + 1)):
        if n % x == 0:
            return False
    return True


if __name__ == "__main__":
    while True:
        try:
            num = input("Input number: ")
            print("Is it prime: ", is_prime(int(num)))
            break
        except ValueError:
            print("\tCan't parse value", file=sys.stderr)
