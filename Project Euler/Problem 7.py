import math
"""What is the 10001st prime number?"""

def isPrime(num):
    prime = True
    if num == 2:
        return True
    elif num % 2 == 0:
        prime = False
    else:
        for i in range(3, math.floor(num ** 0.5) + 1, 2):
            if num % i == 0:
                prime = False
    return prime

primes = []
i = 2
while len(primes) != 10001:
    if isPrime(i):
        primes.append(i)
    i += 1

print(primes[-1])