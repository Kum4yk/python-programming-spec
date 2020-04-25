import sys

"""
a * x ** 2 + b * x + c = 0
D = b ** 2 - 4 * a * c
x1, x2 = (-b + D ** 0.5) / (2 * a), (-b - D ** 0.5) / (2 * a)  
"""
a, b, c = map(int, sys.argv[1:4])

D = b ** 2 - 4 * a * c
x1, x2 = map(int, ((-b + D ** 0.5) / (2 * a), (-b - D ** 0.5) / (2 * a)))
print(x1, x2, sep="\n")
