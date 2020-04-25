import sys

print(sum(map(int, [0] if len(sys.argv) != 2 else sys.argv[1])))
