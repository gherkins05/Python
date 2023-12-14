import math

def isPrime(value):
    if value < 2:
        return False
    elif value == 2:
        return True
    elif value % 2 != 0:
        prime = True
        for i in range(3, math.floor(value ** 0.5) + 1, 2):
            if value % i == 0:
                prime = False
        return prime
    else:
        return False

def formula(n, a, b):
    return n ** 2 + a * n + b

data = []    #Stores lists [num of primes, a, b]

for a in range(-999, 1000):
    for b in range(-1000, 1001):
        counter = 0
        numOfPrimes = 0
        while isPrime(formula(counter, a, b)):
            numOfPrimes += 1
            counter += 1
        data.append([numOfPrimes, a, b])

extract = [0, None]
for item in data:
    if item[0] > extract[0]:
        extract = [item[0], item[1] * item[2]]

print(extract[1])
