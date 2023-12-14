totalS = 0

def getPowers(n, p):
    s = 0
    for num in [*str(n)]:
        s += int(num) ** p
    return s

for i in range(2, 10000000):
    if i == getPowers(i, 5):
        totalS += i
print(totalS)
