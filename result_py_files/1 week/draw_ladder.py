import sys

value = 0 if len(sys.argv) != 2 else int(sys.argv[1])
for i in range(value):
    i += 1
    print(" " * (value - i), "#" * i, sep="")
