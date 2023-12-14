import math
"""Find the sum of all the primes below 2 million"""
sumOfPrimes = 2
limit = 2000000

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

for i in range(3, limit, 2):
    if isPrime(i):
        sumOfPrimes += i

print(sumOfPrimes)