import math
total = 0

def getSum(n):
    s = 0
    for num in [*str(n)]:
        s += math.factorial(int(num))
    return s


for i in range(3, 1000000):
    if i == getSum(i):
        print(i)
        total += i

print(total)
